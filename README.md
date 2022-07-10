# Todorant TUI

A Todorant client for the terminal written in Python with keyboard control only.

![Demo](https://s8.gifyu.com/images/demo99abae2d82f2ccfd.gif)

# Installation

1. Clone repo
2. `poetry install`
3. Or install from `PyPI` by `pip install todorant-tui`
4. Setup `access_token` environment variable or make `.env` file with it
5. `make run`

# How to get access_token

1. Open [todorant.com](https://todorant.com) website and login
2. Run following code in dev console and copy token
```
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
};
console.log(getCookie('token'));
```

# How to use

The program is controlled exclusively from the keyboard. Pay attention to bold letters. On the planning screen, use the up and down arrows to navigate through tasks and the left and right arrows to navigate through pages.

# Controls

## Current view

* `q` to quit application
* `d` to mark current todo as done
* `e` to edit current todo
* `r` to remove current todo
* `c` to create new todo
* `p` switch to Planning view

## Planning view

* `q` to quit application
* `up` and `down` arrows to navigate through tasks
* `left` and `right` arrows to navigate through pages
* `d` to mark selected todo as done
* `e` to edit selected todo
* `r` to remove selected todo
* `c` to create new todo
* `h` to show/hide completed tasks
* `u` switch to Current view

## Create or Edit view
* `t` to focus on text input
* `d` to focus on date input
* `m` to focus on yearn and month input
* `f` to toggle frog
* `o` to toggle completed
* `b` to go back to previous view
* `c` to create on Create view
* `u` to update on Edit view


# TODO
[x] Todorant API Client

[x] Current and Planning tabs

[x] Create/edit/done/remove todo

[ ] Login form

[ ] Make animations and transition

[x] Publish to PyPI

[ ] Refactor all strings
