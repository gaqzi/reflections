---
title: Distil git logs attached to a single file
date: 2022-06-21
tags: shell, git
---

I run `git log --oneline` to list out the commit logs all the time. It prints out a
compact view of the git history. Running the command in this repo gives me this:

```
d9fad76 Publish blog on safer operator.itemgetter, closes #130
0570997 Merge pull request #129 from rednafi/dependabot/github_actions/...
6967f73 Bump actions/setup-python from 3 to 4
48c8634 Merge pull request #128 from rednafi/dependabot/pip/mypy-0.961
5b7a7b0 Bump mypy from 0.960 to 0.961
```

However, there are times when I need to list out the commit logs that only represent
the changes made to a particular file. Here's the command that does exactly that.

```
git logs --oneline --follow <file_path>
```

Running the command on the markdown file that you're reading gives this:

```
git log --oneline
```

```
f5d2d4a (HEAD -> master) Git log follow post, closes #132
```

Unfortunately, this command doesn't support flag chaining. So, you can't use the
`--follow`` flag multiple times to concatenate the logs for multiple files. But there's
a way to do it via shell command. Here's how:

```
echo "<file_path_1> <file_path_b>" \
    | xargs -n1 \
    | xargs -I{} sh -c "git log --oneline --follow {}; echo ===="
```

Running the command on two random files in this repo yields the following output:

```
echo "pelicanconf.py src.py" \
    | xargs -n1 \
    | xargs -I{} sh -c "git log --oneline --follow {}; echo ===="
```

```
96c0e8c Aesthetics, refs #131
e6d5409 Add default link-sharing image, closes #83
9ed958c SEO
fba05d8 Add footer
8dec778 Transformation
4a402b3 Basic customizations
1c93c23 Add pelican conf
====
b89791f Fix bug in operator itemgetter implementation
c75e2ab Push draft of post on typeguard, refs #87
0c6fc7b Add blacken docs to tool stack
20ac41d Publish amphibian decorators blog, closes #54
b8ab730 Publish blogs on rust-like exception handling in Python, closes #63
====
```

Here, the first `xargs` is used to split the line and extract the two filenames. The
second `xargs` applies the `git log --oneline --follow` command to the two files and
concatenates the output with a `====` separator. The separator helps you figure out
which output came from which file.
