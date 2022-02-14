<h1>Reflections<img src='https://user-images.githubusercontent.com/30027932/149235389-c6b85b40-5515-4de4-a922-7b0f91efd0cf.png' align='right' width='128' height='128'></h1>


<strong>>> <i>Reflections & Snippet Style Notes on Software</i> <<</strong>

</div>

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![github_actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Local Development

Assuming you're using a Unix-based system:

* Clone this repository and head over to the root directory.
* Make sure that you've got Python 3.10 installed in your system.
* Run `make init`. This will create a virtual environment named `.venv`, install the dependencies, and prepare the theme for serving.
* Run `make devserver`. This will serve the contents locally.
* Go to [http://localhost:5000](http://localhost:5000) to see the site.
* The site will hot-reload whenever you make any changes to the content or the configuration files.


## Infrastructure

The site is built using [Pelican](https://github.com/getpelican/pelican) and hosted on Github pages. The CI automatically initiate the build—

* Every day at 1 pm UTC
* On every pull request
* On every push to the master branch

Also, [dependabot](https://github.com/dependabot/dependabot-core) is working tirelessly to keep the dependencies fresh.


## Contributions

If you've spotted an errata and want to fix it, then—

* Fork the repo and headover to the root directory.
* Create a feature branch.
* Update the relevant files in the [content](./content/*) folder. The blogs are written in GitHub flavored markdown.
* Push you changes to your fork.
* Send a pull request against the `master` branch, and you're done.


<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
