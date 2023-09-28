# ToothPaste

## Description

ToothPaste is a pastebin-like online service that allows its users to store text in an easily accessible and shareable way. It also allows interaction between users via chat messages and voting.

ToothPaste has two kinds of users: registered and anonymous. Most of the features are equally available to both of these groups. While logged-in user edits and removes pastes by going to one's list of pastes, anonymous users can do the same by using a link with a secret token.

There are many levels of privacy on ToothPaste. A paste can be completely public and listed on the front page, or it can be hidden and only available with a direct link. Paste can also be set to be only available to its original logged-in owner. Unlisted paste can also be encrypted for additional security, in which case all users are required to enter a decryption key.

Original owner of a paste can grant edit permissions to other users, as well. Anyone who is able to view the paste can see and write chat messages, while original paste owner can also remove them. Logged-in viewers can also give one up or down vote for the paste.

## Installation

### Setup

Start by cloning project repository to your computer and moving to its root directory:

```
git clone https://github.com/PyryL/toothpaste.git
cd toothpaste
```

Next, setup and activate Python environment and install dependencies:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Note:** If `python` or `pip` commands don't work, try `python3` and `pip3` instead.

**Note:** You can exit activated virtual environment with `deactivate` command.

### Database

Now create a new Postgres database and format it with contents of `schema.sql`. How to do this varies a lot based on how Postgres has been installed to you system. Here is a basic example:

```
createdb <DBNAME>
psql -d <DBNAME> -f schema.sql
```

Replace `<DBNAME>` with your database name of choise (`toothpaste` is recommended).

**Note:** If you have installed Postgres with [local-pg](https://github.com/hy-tsoha/local-pg) tool, you need to pass extra option `-h /tmp/` to both of the example commands above.

### Configuration

Create a file called `.env` in the project root directory and set its contents as follows:

```
DATABASE_URL=<DBURL>
SESSION_SECRET_KEY=<SESSIONSECRET>
```

Replace `<DBURL>` with your database URL (propably something like `postgresql:///dbname`).

Replace `<SESSIONSECRET>` with a secret random string.

### Usage

Now ToothPaste is finally ready to use. Start local server by running

```
invoke start
```

Pylint style check can be run with

```
invoke lint
```

## Development

You can find development documentation in [`docs/`](docs/) directory. Roadmap plan can be found on [wiki page](https://github.com/PyryL/toothpaste/wiki/Roadmap).
