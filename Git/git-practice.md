# Git Interview Questions for Senior Backend Engineers

## 1. Git Internals
Q: Explain Git's object model and how Git stores data internally
A: Git's object model consists of:


- Blobs: Store file contents (e.g., "console.log('Hello')" -> blob:a45b...)
  Example: git hash-object hello.js -> creates blob

- Trees: Store directory structures and file metadata
  Example directory:
  src/
    hello.js (blob:a45b...)
    utils/
      helper.js (blob:c78d...)
  -> Creates tree object with pointers to blobs/subtrees

- Commits: Store commit metadata and point to trees
  Example commit:
  tree: abc123 (points to root tree)
  parent: def456 (previous commit)
  author: Jane Doe
  message: "Add hello.js"

- Tags: Point to specific commits with labels
  Example: git tag v1.0 abc123
  Creates tag object:
  object: abc123 (commit hash)
  type: commit
  tag: v1.0
  tagger: Jane Doe

All objects are content-addressed using SHA-1 hashes
Example: echo "Hello" | git hash-object --stdin
-> da39a3ee5e6b4b0d3255bfef95601890afd80709

## 2. Advanced Git Operations
Q: How would you clean up a messy Git history?
A: Key techniques include:
- Interactive rebase (git rebase -i) to squash/reorder commits
- git filter-branch for rewriting history
- git cherry-pick to selectively apply commits
- git reset/reflog to undo mistakes
- git clean to remove untracked files

## 3. Git Workflows
Q: Compare different Git workflows and their use cases
A: Common workflows:
- GitFlow: Feature branches + develop/master branches
  ```
  master    ----M------M----M----->
              /     /      /
  develop   -D-----D------D------->
           /  /  /   /   /  
  feature -F--F--F---F--F-------->
  ```
  Best for: Large projects with scheduled releases. Provides strict controls but adds complexity.

- Trunk-based: Everyone works on master/main
  ```
  main     --F--F--F--F--F-------->
            |  |  |  |  |
  feature   f--f--f--f--f  (short-lived)
  ```
  Best for: Small teams, CI/CD environments. Simplest model but requires strong testing.

- GitHub Flow: Feature branches + main branch
  ```
  main     ----M----M----M-------->
           /   /    /
  feature f---f----f-------------->
  ```
  Best for: Teams using GitHub, continuous deployment. Simple but needs good PR process.

- GitLab Flow: Environment branches + feature branches
  ```
  prod     ----P----P----P-------->
           /   /    /
  staging --S--S----S------------->
         /   /    /
  main  M---M----M---------------->
       /   /    /
  feat f---f----f----------------->
  ```
  Best for: Complex deployments with multiple environments. Good for regulated industries.

- Release branches: For maintaining multiple versions
  ```
  2.0    ----R----H----H--------->
         /
  1.0   R-----H----H------------->
       /
  main M-----M----M--------------> 
  ```
  Best for: Software products with multiple supported versions. Allows hotfixes (H) for each version.

## 4. Git Performance
Q: How would you optimize Git for large repositories?
A: Strategies include:
- Using Git LFS for large files
- Shallow clones (--depth) for partial history
- Sparse checkouts for subset of files
- git gc for garbage collection
- Submodules for code separation

## 5. Git Hooks
Q: How would you implement Git hooks for enforcing standards?
A: Common use cases:
- pre-commit: Lint code, run tests
- commit-msg: Enforce commit message format
- pre-push: Run full test suite
- post-receive: Trigger deployments
- update: Enforce branch policies

## 6. Advanced Merging
Q: How do you handle complex merge conflicts?
A: Techniques include:
- Using merge strategies (recursive, octopus)
- git rerere for reusing resolved conflicts
- Interactive merge tools
- Custom merge drivers
- Rebase vs merge considerations:
  ```
  Merge:
  main   A---B---C---M
         \         /
  feat    D---E---F
  
  Result preserves full history but can be messy
  
  Rebase:
  main   A---B---C
                 \
  feat           D'---E'---F'
  
  Original: D---E---F
  
  Result is linear history but rewrites commits
  ```
  Merge maintains complete history and is safer but creates "merge bubbles".
  Rebase creates cleaner history but requires force push and should not be used on public branches.

## 7. Git Security
Q: What security measures are important in Git?
A: Key considerations:
- Signed commits using GPG
- Protected branches
- Access control (SSH keys, tokens)
- Secrets scanning
- Audit logging

## 8. Git Automation
Q: How would you automate Git operations in CI/CD?
A: Approaches include:
- Git commands in shell scripts
- Using Git APIs
- GitHub Actions/GitLab CI
- Custom Git hooks
- Automated release management

## 9. Distributed Git
Q: How do you manage Git in distributed teams?
A: Best practices:
- Clear branching strategy
- Code review processes
- Pull request templates
- Branch protection rules
- Automated testing

## 10. Git Troubleshooting
Q: How do you recover from Git disasters?
A: Recovery techniques:
- Using git reflog
- Recovering deleted commits
- Fixing bad merges
- Restoring lost branches
- Handling corrupted repositories



## 11. Cherry-Pick and Branch Merging
Q: How do you handle merging a branch after cherry-picking some of its commits?
A: When you need to merge a branch after cherry-picking commits from it, you need to be careful to avoid duplicate commits. Here's the approach:

1. First understand what happens:
   ```
   main    A---B---C---D'---E'  (D' and E' are cherry-picked)
                \
   feature       D---E---F---G
   ```

2. When merging after cherry-pick:
   - Git will detect that D' and E' are equivalent to D and E
   - It will only apply the unique commits (F and G)
   - Use `git merge feature` normally

3. Best practices:
   - Use `git log --cherry-pick` to see differences between branches
   - Consider using `git rebase -i` instead if branch isn't public
   - Document cherry-picked commits in commit messages
   - Be cautious with merge conflicts in duplicate commits

4. Alternative approach:
   - If you want to avoid potential conflicts
   - Cherry-pick remaining commits individually
   - Then delete the source branch

Note: Cherry-picking followed by merging can make history harder to read, so consider if cherry-picking is really necessary versus a regular merge or rebase.


## 12. Squashing Commits
Q: How do you squash multiple commits into one and push to remote?
A: Here's how to combine multiple commits into a single meaningful commit:

1. Interactive rebase approach:
   ```bash
   # Start interactive rebase going back N commits
   git rebase -i HEAD~N
   
   # In editor, mark commits to squash:
   pick abc123 First commit
   squash def456 Second commit
   squash ghi789 Third commit
   
   # Write new commit message
   # Save and exit
   ```

2. Soft reset approach:
   ```bash
   # Reset to N commits back while keeping changes staged
   git reset --soft HEAD~N
   
   # Create new commit with all changes
   git commit -m "New consolidated commit message"
   ```

3. Force push to remote:
   ```bash
   # Only use force push if branch isn't shared!
   git push --force-with-lease origin branch-name
   ```

Best practices:
- Only squash commits that haven't been pushed to shared branches
- Use --force-with-lease instead of --force for safety
- Write meaningful commit messages summarizing all changes
- Keep commits that represent logical changes separate
- Consider team workflow before squashing shared history

Note: Be extremely careful with force push as it rewrites history. Never force push to main/master or shared branches without team agreement.
