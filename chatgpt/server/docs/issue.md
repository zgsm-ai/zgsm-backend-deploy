#### Logger not outputting logs in some scenarios

Discovery date: 2023-12-28

Discovered by: Liu Peng z10807

Fix date:

Fixed by:

Issue description: In some files, logger is used to output logs, but they are not actually output

Root cause: In the app.py startup file, register_logger() operation is executed after importing those modules

Solution: Keep the startup file clean, move business code out
