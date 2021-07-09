# Unittest master class

> This is a complementary repo for Unittest training I provided. Files and examples can be used freely.

The programs we going to test are "Patterns" - apps that discover and model some existing software on the local machine (where the program runs). These examples designed to be at least a bit similar to [BMC Discovery patterns](https://docs.bmc.com/docs/discovery/112/the-pattern-language-tpl-788121531.html).
To offload the complexity I've created the helper module (`main`) with base abstract class `Software` for creating "Pattern" subclasses.

This repo has two examples of patterns - `SSHClient` and `DockerDesktop`.

So, `Pattern` is class used to model some piece of software installed/running in the system, it is a subclass of `Software` which has some abstract methods required to be implemented:

* get_type
    * Returns str - the type of discovered software
* get_name
    * Returns str - the name/instance ID of discovered software
* get_version
    * Returns str - the version of discovered software
* get_details
    * Returns dict - the key-valued map of various optional additional details of the discovered software

After new Pattern class has these methods implemented, it is possible to discover the software via running it's `discover` method (implemented in base class). This inherited discover method will automatically run those methods and print out the software detailed information.

I'm going to add unit tests to this repo during or a bit of prior to the actual live session.
