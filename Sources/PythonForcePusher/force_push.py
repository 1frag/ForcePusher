import os
import sys

from github import Github


def _main():
    token = input('Token: ')
    owner = input('Owner: ')
    repository = input('Repository: ')
    no_signed = '--no-signed' in sys.argv

    g = Github(token)
    repo = g.get_repo('/'.join([owner, repository]))
    pr = repo.get_pull(int(input('Номер PR: ')))

    if not (pr.assignee and pr.assignee.login == input('Assignee: ')):
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
