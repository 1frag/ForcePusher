import json
import os
import sys

from github import Github

fields_config = ['token', 'owner', 'repository', 'login']


def get_config():
    config = {}
    gh_proc = os.popen('gh api user')
    for source in (os.environ['HOME'] + '/.push.json', gh_proc.name):
        try:
            config.update(json.loads(open(source).read()))
        except:
            pass
    try:
        owner, repository = os.popen('git config --get remote.origin.url')\
            .read() \
            .removeprefix('git@github.com:') \
            .removesuffix('.git') \
            .split('/')
        config['owner'], config['repository'] = owner, repository
    except:
        pass
    return {k: config.get(k) for k in fields_config}


def _main():
    config = get_config()
    token = config['token'] or input('Token: ')
    owner = config['owner'] or input('Owner: ')
    repository = config['repository'] or input('Repository: ')
    assignee = config['login'] or input('Assignee: ')
    no_signed = '--no-signed' in sys.argv
    pr_number = int(input('PR number: '))

    g = Github(token)
    repo = g.get_repo('/'.join([owner, repository]))
    pr = repo.get_pull(pr_number)

    if not (pr.assignee and pr.assignee.login == assignee):
        print("is the pull request yours?")
        exit(1)

    from_branch, to_branch = pr.head.ref, pr.base.ref
    out = os.popen(f'cd /tmp '
                   f'&& rm -rf {repository} '
                   f'&& git clone {repo.ssh_url} '
                   f'&& cd {repository} '
                   f'&& git checkout origin/{to_branch} '
                   f'&& git diff origin/{to_branch} origin/{from_branch} | git apply '
                   f'&& git add . '
                   f'&& git commit {"" if no_signed else "-S"} -m {pr.title!r}').read()

    if input(out + ' ok? ') == 'yes':
        print(os.popen(f'cd /tmp/{repository} && git push origin HEAD:{from_branch} --force').read())
    else:
        print('cancelled')


def main():
    try:
        _main()
    except KeyboardInterrupt:
        exit(1)
