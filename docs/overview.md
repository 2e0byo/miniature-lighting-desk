Your miniature lighting controller is controlled over USB, using a custom (but
very simple ad documented) protocol.  USB is a *good* way to control hardware:

- it is ubiquitous
- it is fast
- it has high reliability (inbuilt packet error checking)

Unfortunately, USB requires wires.  When you are running around a studio, it
would be nice to be able to control the controller from anywhere:

- via an app
- via a web browser
- via software running on the computer connected (via USB) to the controller.

`miniature-lighting-desk` exists to make this possible.  It provides a *server*
which communicates with a miniature controller over USB (leveraging the same
code shipped with the original `miniature-lighting-controller`) and with various
frontend clients.  This server can handle multiple connections, locally and over
a network.  Network and local frontends are supplied (although the local
frontend is now deprecated, and no further development will be done.**

## The Server

runs on a computer connected to the controller.  This computer does not need to
be a standard 'computer': it could be a Raspberry Pi, a wireless router (running
something like `openwrt`), anything.  The only requirement is that it can run
the server, i.e. it needs a recent python and a network connection.

## The Local Frontend

is identical to the previous software. It is provided for familiarity. No
further development will be done on it, as the web frontend is also useable
locally.

## The Web Frontend

is written in `Node.js` and looks a great deal better than the old frontend.
Functionality can be added to it very easily without affecting the backend
server.


