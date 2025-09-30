[![Documentation](https://img.shields.io/badge/documentation-online-blue.svg)](https://libsms.readthedocs.io/en/latest/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1UOA_qy_jprxKjsVewNrefiyGw7z_981D?usp=sharing)
[![CI](https://img.shields.io/github/actions/workflow/status/AlexPatrie/libsms/ci.yml?branch=main)](https://github.com/AlexPatrie/libsms/actions/workflows/ci.yml?query=branch%3Amain)

### Regarding SMS API:

The SMS(Simulating Microbial Systems) API allows users to design, run, and analyze reproducible simulations of dynamic cellular processes in Escherichia coli.
This tool aims to allow users to configure, run, and introspect simulations of the vEcoli(Vivarium-Ecoli) model. The SMS API uniquely acts as both a server
and client, using FastAPI, Uvicorn, and Marimo to serve a REST API as well as host Marimo user interfaces. The full comprehensive REST API documentation is
available at https://sms.cam.uchc.edu/redoc. Please refer to the aforementioned documentation for the complete details of the request query parameters and
body data required for each outlined endpoint.

Server-side sits kubernetes cluster containing a containerized ASGI(Asynchronous Server Gateway Interface) application using Python and FastAPI which is hosted and
available at https://sms.cam.uchc.edu/. An API router of endpoints is assigned for each API in this project's scope and available by name in the request url. The
primary modes of interaction exist within the "/wcm" and "/core" endpoint routers. For example, the primary single-cell API ("core") endpoints are hosted at https://sms.cam.uchc.edu/core.
A more generalized, Nextflow-based group of endpoints that is actively being developed is available at https://sms.cam.uchc.edu/wcm. Internally it uses a simulation service
that dynamically creates and dispatches SLURM job scripts which are executed through an authenticated connection with a given HPC(High Performance Computing) environment.

The /wcm endpoint router enables the design, execution, and introspection of simulations using vEcoli's Nextflow API. This is the preferred mode of interaction with
the SMS API, as it enables users to customize simulation configurations, create variants, run analysis, and execute a "batch" of one or many ecoli simulation jobs.
A typical end-to-end SMS API /wcm workflow consists of the following:

This project’s “client” behavior is leveraged by the utilization of Marimo(python) components rather than a traditional javascript-based frontend framework. A
static HTML Jinja template is served as an extension of the FastAPI/Uvicorn backend server enabling interactive simulation introspection. There exists a user
interface for each router within the set of routers exposed by the REST API. The user interface makes calls to the REST API to enable non-programmatic interaction
with the aforementioned endpoints. This UI is accessible by navigating to https://sms.cam.uchc.edu/.
