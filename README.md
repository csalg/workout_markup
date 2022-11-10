Workout Markdown is a convention for writing markdown to log training sessions.

It's intuitive to write, renders ok on a browser, and can be understood by a computer.

Originally it was called "Workout Markup" and it was a really good idea with very poor execution. This is my more attempt at being more down-to-earth.

It will be written in go.

## Usage
### Creation

Creation is a bit like js, just create a new log from scratch. Create the document, then fill it out while you train. Name it `<name of training>-<iso date>.md` (see `/examples`).

The second time instead of writing the whole thing again, type `workout` or `wo` and you will get a `fzf` list with the different routines that are logged. Pick one and a new document will be created and open in `nvim` with the previous results. 

So basically creation is by cloning.

And for now that is really the extent of the scope...
