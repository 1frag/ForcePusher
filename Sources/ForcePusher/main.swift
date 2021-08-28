import OctoKit
import Foundation
import Commands

#if os(Linux)
import Glibc
#else
import Darwin.C
#endif

let input = {(prompt: String) -> String in print(prompt, terminator: ": "); return readLine()!}

let token = input("Token");
let config = TokenConfiguration(token)

let owner = input("Owner")
let repository = input("Repository")
let pr_number = Int(input("Pull request number"))!

var pr: PullRequest?
var repo: Repository?

var sem = DispatchSemaphore.init(value: 0)
Octokit(config).pullRequest(owner: owner, repository: repository, number: pr_number) { pr_resp in
    Octokit(config).repository(owner: owner, name: repository) { repo_resp in
        sem.signal()
        if case .success(let _pr) = pr_resp { pr = _pr }
        if case .success(let _repo) = repo_resp { repo = _repo }
    }
}!.resume(); sem.wait()

if pr == nil {
    print("pull request not found")
    exit(1)
}

if pr!.assignee == nil || pr!.assignee!.login! != input("Assignee") {
    print("is the pull request yours?")
    exit(1)
}

let (from_branch, to_branch) = (pr!.head!.ref!, pr!.base!.ref!)
let result = Commands.Bash.run("""
cd /tmp \
&& rm -rf \(repository) \
&& git clone \(repo!.sshURL!) \
&& cd \(repository) \
&& git checkout origin/\(to_branch) \
&& git diff origin/\(to_branch) origin/\(from_branch) | git apply \
&& git add . \
&& git commit -m '\(pr!.title!)'
""")
print(result.reponse.errorOutput, result.reponse.output, "\nok?")

if readLine()! == "yes" {
    Commands.Bash.run("cd /tmp/\(repository) && git push origin HEAD:\(from_branch) --force")
} else {
    print("cancelled")
}
