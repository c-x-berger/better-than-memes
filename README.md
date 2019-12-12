`better-than-memes`
===
`better-than-memes` is an unholy fusion of Reddit/the idea of threaded comments
and [Usenet's](https://en.wikipedia.org/wiki/Usenet) "board/topic hierarchy."

It is, in a way, the _worst_ of both worlds, being centralized like Reddit and
obsessively "organized" like Usenet. ~~Hopefully the centralized part goes away
soon.~~

Setup
---
Why would you want to do this?

You'll need to have a PostgreSQL database up and running. Edit `POSTGRES_CONFIG`
in `config.py` to match the details to connect to your database.

To create the required tables, execute `setup.sql` on your database. This will
create tables for comments, posts, users, etc.

Once your database is setup, install the required Python libraries with
something like `pip install -r requirements.txt`. You should then be able to
run `better-than-memes` with any [ASGI](https://github.com/django/asgiref/blob/master/specs/asgi.rst)
server - though because `better-than-memes` is based on Quart, the "official"
recommendation is to use [Hypercorn.](https://gitlab.com/pgjones/hypercorn)
```shell script
# start hypercorn server
hypercorn app:app
```