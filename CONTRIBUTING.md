Contributing to NEPC
====================

`nepc` is an open source project, and you are welcome to contribute to its development. Contributions can come in any areas: writing code, contributing example fictitious data and data analysis, writing documentation, adding and improving tests (including providing interesting yet realistic fictitious electron scattering data and new failing tests for desired features), cleaning up code (i.e. improving the pylint score),  etc.

Version control of `nepc` is done with `git`. We use a continuous integration system and monitor code quality. 

Reporting Issues
----------------

When opening an issue to report a problem, please try to provide a minimal code
example that reproduces the issue along with details of the operating
system and package versions that you are using (relative to the `nepc-dev` conda
environment provided in `environment-dev.yml`).

Contributing Code
-----------------

So you are interested in contributing code to the NEPC Project? Excellent!
We love contributions! NEPC is open source, built on open source,
and we'd love to have you hang out in our community.

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not
ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at
all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect code
isn't the measure of a good developer (that would disqualify all of us!); it's
trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can
help out by writing documentation, tests, or even giving feedback about the
project (and yes - that includes giving feedback about the contribution
process). Some of these contributions may be the most valuable to the project as
a whole, because you're coming to the project with fresh eyes, so you can see
the errors and assumptions that seasoned contributors have glossed over.

Note: This disclaimer was originally written by
[Adrienne Lowe](https://github.com/adriennefriend) for a
[PyCon talk](https://www.youtube.com/watch?v=6Uj746j9Heo), and was adapted by
Astropy based on its use in the README file for the
[MetPy project](https://github.com/Unidata/MetPy) and then further adapted for NEPC.

Most contributions to NEPC are done via pull requests from GitHub users'
forks of the [nepc repository](https://github.com/USNavalResearchLaboratory/nepc).

Once you open a pull request (which should be opened against the ``master``
branch, not against any of the other branches), please make sure to
include the following:

- **Code**: the code you are adding

- **Tests**: these are usually tests to ensure code that previously
  failed now works (regression tests), or tests that cover as much as possible
  of the new functionality to make sure it does not break in the future.

- **Documentation**: documentation is generated using 
  [Sphinx](http://www.sphinx-doc.org/en/master/index.html), so 
  all source code should be commented with docstrings. Follow the NumPy conventions 
  outlined in the 
  [numpydoc docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html) 
  for all docstrings.  Build and check documentation locally before making pull requests.

- **Changelog entry**: whether you are fixing a bug or adding new
  functionality, you should add an entry to the ``CHANGES.rst`` file that
  includes the PR number. If you are opening a pull request, you may not know
  the PR number yet, but you can add it once the pull request is open. If you
  are not sure where to put the changelog entry, wait until a maintainer
  has reviewed your PR and assigned it to a milestone.

  You do not need to include a changelog entry for fixes to bugs introduced in
  the developer version and therefore are not present in the stable releases. In
  general you do not need to include a changelog entry for minor documentation
  or test updates. Only user-visible changes (new features/API changes, fixed
  issues) need to be mentioned. If in doubt, ask the core maintainer reviewing
  your changes.

<!--
Other Tips
----------

- To prevent the automated tests from running, you can add ``[ci skip]`` to your
  commit message. This is useful if your PR is a work in progress and you are
  not yet ready for the tests to run. For example:

      $ git commit -m "WIP widget [ci skip]"

  - If you already made the commit without including this string, you can edit
    your existing commit message by running:

        $ git commit --amend

- To skip only the tests running on GitHub Actions use ``[skip github]``.

- If your commit makes substantial changes to the documentation but no code
  changes, then you can use ``[skip github]``, which will skip GitHub Actions CI
  because documentation build is done on CircleCI. The exception to this rule
  is when your changes to documentation include code snippets that need to
  be tested using ``doctest``.

- When contributing trivial documentation fixes (i.e., fixes to typos, spelling,
  grammar) that don't contain any special markup and are not associated with
  code changes, please include the string ``[skip github]`` in your commit
  message.

      $ git commit -m "Fixed typo [skip github]"
-->


Checklist for Contributed Code
------------------------------

A pull request for a new feature will be reviewed to see if it meets the
following requirements. For any pull request, a `nepc` maintainer can help
to make sure that the pull request meets the requirements for inclusion in the
package.

**Scientific Quality** (when applicable)
  * Is the submission relevant?
  * Are references included to the origin source?
  * Does the code perform as expected?
  * Has the code been tested against previously existing implementations?

**Code Quality**
  * Is the code compatible with Python >=3.6?
  * Are there dependencies other than the `nepc` core, the Python Standard
    Library, and NumPy 1.16.0 or later?
    * Is the package importable? 
    * Are additional dependencies handled appropriately?
    * Do functions that require additional dependencies raise an `ImportError`
      if they are not present?
  * Run a linter before making pull requests. `nepc` CI uses `pylint`. See 
    [note below on running `pylint` in your conda environment](#pylint-in-a-conda-environment).

**Testing**
  * Are the inputs to the functions sufficiently tested?
  * Are there tests for any exceptions raised?
  * Are there tests for the expected performance?
  * Are the sources for the tests documented?
  * Have tests that require an optional dependency been marked as such?
  * Does ``pytest --local`` run without failures? See [nepc documentation: Accessing a NEPC MySQL Database](https://nepc.readthedocs.io/en/latest/mysql.html) for help on setting up a local `nepc_test` database.

**Documentation**
  * Is there a docstring in [numpydoc format](https://numpydoc.readthedocs.io/en/latest/format.html) in the function describing:
    * What the code does?
    * The format of the inputs of the function?
    * The format of the outputs of the function?
    * Any exceptions which are raised?
    * An example of running the code?
  * Is there any information needed to be added to the docs to describe the function?
  * Does the documentation build with sphinx without errors or warnings? See 
    [note below on using `livereload`](#livereload).

**License**
  * Is the `nepc` license included at the top of the file?
  * Are there any conflicts with this code and existing codes?

**NEPC requirements**
  * Do all the CI tests pass?
  * If applicable, has an entry been added into the changelog?
  * Can you check out the pull request and repeat the examples and tests?

Nuts and Bolts
==============

Development Environment
-----------------------

Developing `nepc` works best within a conda environment (`environment-dev.yml` file provided). 
Also, if you are going to build a database yourself, you will need MySQL. To get started:

```console
$ git clone https://github.com/USNavalResearchLaboratory/nepc.git
$ cd nepc
$ conda env create -f environment-dev.yml #create the nepc-dev conda environment 
$ conda activate nepc-dev
$ pip install -e . # install the nepc package and sub-packages into the nepc-dev conda environment
$ export NEPC_HOME=/path/to/cloned/nepc/repo/ # in your `~/.bashrc` or `~/.bash_profile` or other appropriate shell config
$ pytest --local # requires the nepc_test database (see note below)
```
*Note: running pytest --local requires a nepc_test database and MySQL server. See [the nepc docs](https://nepc.readthedocs.io/en/latest/mysql.html) for help on building the `nepc_test` database.*

`pylint` in a conda environment
-------------------------------

It's probably best to make sure `pylint` is not in your base conda environment. Otherwise, when you run `pylint`, the linter will give you errors and warnings for your base environment, not your `nepc-dev` conda environment.  (i.e. run `conda uninstall pylint` in your base conda environment, if necessary.)

`livereload`
------------

The very useful tool [`livereload`](https://livereload.readthedocs.io/en/latest/) for monitoring
changes in Sphinx documentation in real-time is included 
in the `nepc-dev` conda environment (`environment-dev.yml` file). 
Here’s a simple script that detects changes in any `*.rst` files in `doc` or `*.py` files in `nepc`,
rebuilds the Sphinx documentation, and starts a `livereload` server:

```python
#!/usr/bin/env python
from livereload import Server, shell
import formic

PATTERNS = ["doc/**.rst", "nepc/**.py"]

SERVER = Server()
for filepath in formic.FileSet(include=PATTERNS):
    SERVER.watch(filepath, shell('make html', cwd='doc'))
SERVER.serve(root='doc/_build/html')
```

Run it inside the root directory of the `nepc` repo, then open 
[http://localhost:5500/](http://localhost:5500/), and you can see any
documentation changes you are making in real time.

Sphinx cross-references
-----------------------

If you are having trouble determining the syntax for a Sphinx cross-reference (internal
or external), try the command-line tool [https://github.com/bskinn/sphobjinv](sphobjinv),
which is included in the `nepc-dev` conda environment (`environment-dev.yml` file).
