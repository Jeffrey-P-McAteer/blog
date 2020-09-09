
# The Best Tools for a Job

Computer science is a rapid, chaotic environment.
Making sense of the jobs we have to perform and the
tools that are appropriate for a given task becomes a
science unto itself.

Fortunately there exist some shining tools which rise above
the rest and are the first tool you should pick given
a matching task.


======================================================

## Data Storage

### Local Application Data with a Schema

Use `sqlite3`:

 - [sqlite.org](https://www.sqlite.org/index.html)

Sqlite is embedded in your application and runs as part of your process.
Data is stored in a single file and sqlite can handle multiple processes
reading and writing to the same database file at the same time.


### Local Application Data without a Schema

Use `unqlite`:

 - [unqlite.org](https://unqlite.org/)

Unqlite is embedded in your application and runs as part of your process.
Data is stored in a single file and unqlite can handle multiple processes
reading and writing data to the same database file at the same time.

### Remote Application Data with a Schema

Use `postgres`:

 - [postgresql.org](https://www.postgresql.org/)

Postgres runs as a system service and provides a huge number of ways to
talk to the database, but for data with a schema you will be using prepared SQL statements
and will most likely connect over tcp to port 5432.

### Remote Application Data without a Schema

Use `postgres`:

 - [postgresql.org](https://www.postgresql.org/)
 - [presentation on unstructured data types in postgres](http://leopard.in.ua/presentations/udck_2017/index.html)

Postgres has full support for unstructured data, so as long as your application can handle
lists/maps/graph type data you can use a postgres connection to read and write those kinds of data.


======================================================

## Message Formats

### With a Schema, Binary

Use `BARE`:

 - [baremessages.org](https://baremessages.org/)

BARE is very similar to how any C compiler will lay out data in memory,
but the utility here is that BARE is a standard so you can
send data represented in a C program to a Python program so
long as both programs use the same BARE schema source files.

### Without a Schema, Binary

Use `CBOR`:

 - [cbor.io](https://cbor.io/)
 - [Read RFC 7049](https://tools.ietf.org/html/rfc7049)

CBOR is essentially a standard format for lists, maps, and primitives
like strings, integers, and floating-point numbers.


### With a Schema, Human Readable

Use `TOML`:

 - [github.com/toml-lang/toml](https://github.com/toml-lang/toml)

### Without a Schema, Human Readable

Use `TOML`:

 - [github.com/toml-lang/toml](https://github.com/toml-lang/toml)


======================================================

## Application Graphics

### Gaming/Heavy custom visuals

Use the `godot` engine:

 - [godotengine.org](https://godotengine.org/)

The godot engine contains all the features you'd need for 3d/physics/custom
graphics while still compiling to an embeddable game engine which lets you ship
a single .exe file to customers.

### Text and Image-based User Interfaces

Use a `webview`:

 - [github.com/webview](https://github.com/webview/webview)
 - [JavaFX WebView](https://docs.oracle.com/javase/8/javafx/api/javafx/scene/web/WebView.html)

Assuming your software will be used on more than one OS and that the UI will be modified,
paying the cost of a web view will give you native-enough graphics without a large
infrastructure cost. Usually you will link against the system web view which means not
having to pay the cost of embedding a web engine in your application, as well as faster startup times.


======================================================

## Remote Graphics

### User Applications/Desktop Environments

use Microsoft's `RDP`:

 - [wikipedia.org/Remote_Desktop_Protocol](https://en.wikipedia.org/wiki/Remote_Desktop_Protocol)
 - [freerdp.com](http://www.freerdp.com/)

RDP includes side channels for sending just an application window,
but this is highly proprietary. Still the protocol quality is so good
it is worth mentioning here.

X11 should also be mentioned here because it is the best choice
for environments where applications being sent are mostly text
and buttons. X11 is more flexible than RDP to deploy and it has
a simpler authentication system, but it performs poorly with large
images or animated pixels.

### Video Streams

The jury is still out, there are many video encoding and playback systems.
None stand out enough to warrant inclusion here, that decision should be
made based on what systems are being targeted and how the video will be used.


======================================================

## Backups

### File Granularity

Use `rsync`:

 - [wikipedia.org/Rsync](https://en.wikipedia.org/wiki/Rsync)

Rsync is a time-tested file delta transmission tool. For backup purposes
use the `--link-dest=/backup-N-1/` flag to create hard links for files which
do not need to be transferred because they have not changed from backup `N-1` to `N`.

A related (but less performant) tool is [Rclone](https://rclone.org/) which may be
used to standardize cloud storage pools.

### Block Device Granularity

Don't do this. If your backups can be called "images" you need
to re-evaluate how your infrastructure is assembled, because
it sounds like the procedure is:

> stick an install CD in, click next next next, then image the thing so if it breaks we can go back

Which stopped being an effective tactic when good operating systems (linux, 1991 or freebsd, 1993) and filesystems (xfs, 1994)
were created, and it becomes an even less effective tactic when one realises containers (bsd jails, 2000 or cgroups, 2006) exist.

Please use one or a combination of those 3 tools because all of them allow you to backup the important pieces of a system
and replace the non-important pieces of a system when the non-important pieces become non-functional.


======================================================

## Remote Procedure Calls

### For Applications

The jury is still out, no systems standardize data formats and return values well enough to be included here.


### For Humans

use `ssh`:

 - [wikipedia.org/Secure_Shell](https://en.wikipedia.org/wiki/Secure_Shell)


SSH has proven to be a flexible and robust tool for authenticating users and presenting
them with a shell, x11 forwarding, and arbitrary port forwarding. A server owner
may specify user control limits, run custom code when users connect, and SSH can use the PAM
system to authenticate against kerberos/ldap/OTP 2 factor systems.

SSH is also the backbone of most `rsync` and `git` systems, and windows 10 has started shipping with a client installed (\~2018?).


======================================================

## Geospatial Mapping

The jury is still out, no systems standardize geospatial visuals and processing well enough to be included here.







