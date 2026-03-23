# Git Basics Cheat Sheet

## What is Git?
Git is a distributed version control system that tracks changes in source code during software development. It was created by Linus Torvalds in 2005 for Linux kernel development. Git allows multiple developers to work on the same project simultaneously without overwriting each other's changes. Every developer has a full copy of the repository history on their local machine.

## Basic Commands
The most essential Git commands are git init to create a new repository, git clone to copy an existing repository, git add to stage changes, git commit to save staged changes with a message, and git push to upload commits to a remote repository. Use git status to see the current state of your working directory and git log to view commit history.

## Branching and Merging
Branches allow you to develop features in isolation from the main codebase. Create a new branch with git branch feature-name and switch to it with git checkout feature-name, or combine both with git checkout -b feature-name. When your feature is complete, merge it back with git merge feature-name from the main branch. If two branches modify the same lines, Git will report a merge conflict that you must resolve manually.

## Git Rebase
Rebasing is an alternative to merging that creates a linear commit history. Use git rebase main while on your feature branch to replay your commits on top of the latest main branch. This makes the history cleaner but should never be done on public branches that others are working on. Interactive rebase with git rebase -i allows you to squash, reorder, or edit commits before finalizing.

## Git Stash
Git stash temporarily saves uncommitted changes so you can switch branches without committing incomplete work. Use git stash to save changes, git stash list to see all stashes, git stash pop to restore the most recent stash, and git stash drop to delete a stash. This is useful when you need to quickly switch context to fix a bug on another branch.

## Pull Requests and Collaboration
A pull request is a way to propose changes from your branch to the main branch. On platforms like GitHub and GitLab, you create a pull request after pushing your branch. Team members review the code, leave comments, and approve or request changes. Once approved, the pull request is merged. This workflow ensures code quality through peer review and is standard practice in professional development teams.

## Undoing Changes
To undo the last commit but keep changes staged, use git reset --soft HEAD~1. To unstage files, use git reset HEAD filename. To discard all local changes in a file, use git checkout -- filename. The git revert command creates a new commit that undoes a previous commit without rewriting history, making it safe for shared branches.
