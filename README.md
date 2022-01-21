<h1>Reflections<img src='https://user-images.githubusercontent.com/30027932/149235389-c6b85b40-5515-4de4-a922-7b0f91efd0cf.png' align='right' width='128' height='128'></h1>


<strong>>> <i>Reflections & Snippet Style Notes on Software</i> <<</strong>

</div>

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![github_actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Local Development

Assuming you're using a Unix-based system.

* Clone this repository and head over to the root directory.

* Make and activate a Python 3.10 virtual environment.

* Install the dependencies via running:

    ```
    pip install -r requirements.txt
    ```
* Run `make devserver`.

* Go to [http://localhost:5000](http://localhost:5000) to see the site locally.

* The site will hot-reload if you change any files in the `content` and `theme` directory, or any of the configuration files.


## Infrastructure

The site is built using [Pelican](https://github.com/getpelican/pelican) and hosted on Github pages. The CI automatically builds the site—

* Every day at 1 pm UTC
* On every pull request
* On every push to the master branch

Also, [dependabot](https://github.com/dependabot/dependabot-core) is working tirelessly to keep things fresh.


## Contributions

If you've spotted an errata and want to fix it, then—

* Update the relevant files in the [content](./content) folder. The blogs are written in GitHub flavored markdown.
* Send a pull request against the `master` branch, and you're done.


<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
