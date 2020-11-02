
# My Favorite Languages

1. **Rust**

Rust stands as the all-time champion in terms of code quality,
both the language grammar and the tooling that rust's
community has built.

Rust can cross-compile easily (incl. exotic targets like `wasm32-unknown-unknown`),
interacts with native code easily, has first-class support for lifetimes, and contains
the second-best macroing system in the world (Zig's `comptime` takes first place but has
it's own downsides because of how much it is used).

For any new systems of moderate complexity I find myself reaching for Rust because
it has a large set of libraries, great tooling, and I know the compiler will
make stupid mistakes nearly impossible which lets me focus on the design of the system
without having to shoehorn in protections against null pointers & friends.

2. **C**

C is still relevant in 2020 because existing systems
are written in C. For small, local projects C can quickly process whatever
you need it to do (eg payroll systems, task managers, simulating economies at scale, and videogames).

For larger projects C must have additional tooling; look at what the linux kernel uses!
If you have access to the tooling necessary there's nothing stopping you from writing
operating systems in C, but for now it's primary purpose is to interact with and extend
existing operating systems, which it does very well.

C is also relevant because it's ABI is the most stable in the world; at the moment
the C ABI is the only ABI respected by every language and every OS.


3. **Python**

Python 3 is my all-time favorite scripting environment.
If you need to process \~10gb of data across \~1000 3rd-party
processes or remote systems, reach for 500 lines of python.

Python is also great for filling tooling gaps; I commonly have a
`build.py` script where `cargo` and `make` fall short because building
the project requires downloading a binary SDK which I don't want
to check into version control.


4. **POSIX Shell**

For small projects which use mostly 3rd-party tools
on unix systems `/bin/sh` is great. There isn't much to say
about it as a language but everyone knows how valuable having
portable shell scripts is and POSIX is the best standard
that the world has been able to agree to.


## Runners up

These languages are nice when you have existing projects,
3rd party requirements, or for some reason the deployment plan
just plays nicely with the language (eg existing Tomcat servers).

Otherwise these are strictly 2nd-tier languages.

1. **Java**

> "Nobody ever got fired for picking Java"

Java has runtimes for many platforms, a decent assortment of (aging) libraries,
and enough tooling to make several nooses from.

Usually this is picked because of environment; there may be existing business
logic in Java that needs a small extension, or you may have a deployment target
that can use `.jar`/`.war` applications quickly.

**C#** falls into this category for me as well but I'm still learning it;
C# appears to have better tooling available.

2. **s**













