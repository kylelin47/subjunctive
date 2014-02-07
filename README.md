**Subjunctive** – a *tile-based puzzle game* engine for Python 3

Note: Subjunctive's API is **not at all stable**. We are still in the
early development stages and things are likely to change a lot!

* * *

## Status of the games

### Think Green

**Think Green** is complete except for the following things, which are
totally missing:

*   title screen / death screen
*   score display
*   music

### Floorpaint

**Floorpaint** has partially complete level-file-loading, but that's
about it. It is missing:

*   core game mechanics (currently you can cross over your path)
*   level generation
*   graphics
*   title screen / instructions
*   music

## Set-up

### Dependencies

**Subjunctive** requires:

*   [Git]
*   [Python 3.3+] and (optional, but recommended) [virtualenv]
*   [sdl2], [sdl2_image], [sdl2_mixer]

> **Hint:** If you're not already using Linux, now would be a good time
> to consider doing so. Installing all this stuff would be as simple as
>
>     $ pacman -S git python3 python3-virtualenv sdl2 sdl2_gfx sdl2_image sdl2_mixer

To get all everything set up, clone our repository, create a virtualenv,
and install dependencies:

    $ git clone https://github.com/ufgmg/subjunctive
    $ cd subjunctive
    $ virtualenv .env
    $ .env/bin/pip install -e .

### Running the games

After installing as described in the previous section, you can run the
games like so:

    $ .env/bin/<game>.py

For example,

    $ .env/bin/think-green.py

### Adding a new game

Add your game's script to the `scripts` list in `setup.py`. Then, re-run

    $ .env/bin/pip install -e .

## Goals / design principles

Obviously the main goal is that it be *significantly* easier to
implement a game with Subjunctive than without. To accomplish that, here
are some general design principles:

*   Provide sane and useful defaults.
*   Make it easy to override defaults.
*   Let client code be as beautiful and succinct as possible.

And, as usual, [the Zen of Python] provides excellent guidance.

## Contributing

### Guidelines

#### Code/text format

*   **Indent with spaces (four per indentation level).** Make sure your
    editor inserts spaces when you press the Tab key.

*   **Read [PEP 8].**

*   **Use UNIX-style line endings.** Make sure your editor saves files
    with UNIX line endings (or that Git is [configured to normalize line
    endings when you
    commit](https://help.github.com/articles/dealing-with-line-endings)).

*   **Avoid trailing whitespace.** This means that blank lines cannot
    not contain any spaces or tabs! You can set up your editor to
    highlight or automatically remove trailing whitespace.

*   **Make sure the file ends with a newline.** `git diff` will show if
    you are about to commit a file with the newline removed. The reason
    for this is that many UNIX-style command-line tools think of the
    newline as a *terminator* rather than a separator. I think this
    interpretation is better in the majority of cases (one such case is
    concatenating two files: `cat <file> <file2>`).

    The crux of the matter is that you must make sure your editor writes
    a newline at the end of the file (if necessary, leave a blank line
    at the end).

#### Commit messages

Refer to [A Note About Git Commit Messages].

### Set-up for contributing

So, you want to help out? It's pretty easy, but there are a few things
you need to set up first.

1.  **Python**

    You need Python 3.3 or newer. You should be able to open a terminal
    and run the Python interpreter by typing `python` or `python3`.

    If you already know some programming, the official [Python Tutorial]
    will teach you the basics. Be sure to run the Python interpreter and
    *try the examples as you read*! If you don't know any programming
    yet, [Codeacademy's Python track] is a good place to start.

2.  **Git**

    Install the standard Git from <http://git-scm.com/downloads>. Unless
    you know better, use the default options. If you're on Windows, you
    should also install the [Git credential helper] so you don't have to
    enter your username and password every time.

    If you have never used Git before, I recommend [Ry's Git Tutorial]
    to learn the basics. If you already know the basics but need a
    reference (and you find the manual pages too confusing), look at
    [Git Reference].

    On Linux or Mac OS, you'll run Git commands using any terminal
    program. On Windows, you'll use **Git Bash** (which was installed
    with Git).

    Don't forget to configure Git with your name and email address:

        $ git config --global user.name "John Smith"
        $ git config --global user.email "johnsmith@juno.com"

    Note that this email address will be publicly viewable through
    GitHub.

3.  **GitHub**

    Create an account on [GitHub] and log in. Make sure the email that
    you configured Git with is associated with your account (you can
    associate additional email addresses in the account settings).

    Navigate to this page and click the *Fork* button. Once the process
    completes, look down the right side of the page for the *clone URL*
    (on Windows you'll want the HTTPS URL; on Linux or Mac OS you
    probably want the SSH URL). Use this to clone the repository to your
    computer.

        $ git clone <URL>

    This will create a directory called `subjunctive`.

    You'll also want to set up *our* repository as a remote.

        $ git remote add ufgmg https://github.com/ufgmg/subjunctive.git

4.  **your editor**

    I strongly recommend against trying to use an IDE for this
    relatively small project! For Linux, I recommend Vim (if you can
    handle the awesome) or Gedit. For Windows, I recommend [Sublime
    Text] (shareware but awesome) or [Notepad++] (open source).

    Figure out how to set up your editor so that it follows the rules
    mentioned in the Code Guidelines above.

### Git Workflow

1.  **Fetch** the latest commits from all of your remote repositories.

        $ git fetch --all

2.  **Checkout** a new branch for the feature you want to work on,
    starting from the `ufgmg/master` branch.

        $ git checkout ufgmg/master
        $ git checkout -b <new branch name>

3.  **Do stuff.** Write codes, consume foods, etc.

4.  **Commit** as necessary. Some steps are optional.

        $ git status          # See what files have uncommitted changes
        $ git diff            # See your actual changes line-by-line
        $ git add <files>     # Add files to the staging area
        $ git status          # Check that you've staged the right files
        $ git diff --cached   # (paranoid) see the line-by-line staged changes
        $ git commit          # Commit it

5.  Repeat steps 3–4 as necessary.

6.  Maybe **rebase** to include newer commits from other people.

    Say, for example, that a new feature or fix has been committed on
    `ufgmg/master` and you need to incorporate it into your branch.
    Usually the best way to do this is via a rebase.

        $ git fetch --all
        $ git rebase ufgmg/master

    Basically what this does is tries to apply your commits, one at a
    time, on to the commits already on `ufgmg/master`. If conflicts
    occur (which they often do!), the rebase will pause for you to fix
    the issues. Running `git status` liberally during a rebase will help
    you stay sane.

    Note that rebasing causes *your* commits to be re-written (i.e.,
    they get new hashes), so if you've already pushed your branch then
    pushing it again after the rebase will most likely fail (because
    doing so would mean replacing the commits you had pushed earlier).
    If you know no one else is using your branch, you can use the
    `--force` option when you push; alternatively, you can just give
    your branch a new name and then push it.

7.  Repeat steps 3–6 as necessary.

8.  **Push** to your GitHub repository.

        $ git push origin <branch name>

9.  Repeat steps 3–8 as necessary.

10. Maybe **rebase** to clean up your branch's history.

11. Send a **pull request**.

[Git]: http://git-scm.com/
[Python 3.3+]: http://www.python.org/download/
[virtualenv]: http://www.virtualenv.org/en/latest/index.html
[sdl2]: http://www.libsdl.org/download-2.0.php
[sdl2_image]: http://www.libsdl.org/projects/SDL_image/
[sdl2_mixer]: http://www.libsdl.org/projects/SDL_mixer/
[the Zen of Python]: http://www.python.org/dev/peps/pep-0020/
[PEP 8]: http://www.python.org/dev/peps/pep-0008/
[A Note About Git Commit Messages]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
[Python Tutorial]: http://docs.python.org/3/tutorial/introduction.html
[Codeacademy's Python track]: http://www.codecademy.com/tracks/python
[Git credential helper]: http://blob.andrewnurse.net/gitcredentialwinstore/git-credential-winstore.exe
[Ry's Git Tutorial]: http://rypress.com/tutorials/git/index.html
[Git Reference]: http://gitref.org/
[GitHub]: https://github.com/
[Sublime Text]: http://www.sublimetext.com/3
[Notepad++]: http://notepad-plus-plus.org/
