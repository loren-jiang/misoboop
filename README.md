<div align="center">
  <img alt="Logo" src="https://di0n0okh38ak5.cloudfront.net/static/assets/lucky_dumpling_cat_min.svg" width="300" />
</div>
<h1 align="center">
	MisoBoop
</h1>
<h3 align="center">
	American cooking with Chinese roots
</h3>
<p align="center">
	Website featuring personal recipes, blog posts, and my cat, Miso -- built using Django + PostgresSQL backend and simple jQuery/Javascript + Materialize CSS, hosted on Digital Ocean.
</p>

![screenshot](https://di0n0okh38ak5.cloudfront.net/brand/misoboop_ss.png)

## 🚨 Forking this repo (please read!)

Feel free to fork (in most scenarios), but please attribute it back to me -- e.g. linking back to [misoboop.com](https://www.misoboop.com). This isn't intended to be a template website, but so please refer to official documentation for workarounds if needed. 

## Features
- AWS S3 + CloudFront integration for media and static files
- TinyMCE4 integration for easy HTML markup 
- PostgreSQL backend
- Compressed Javascript and (S)CSS files
- Full-text and live searching of recipes 
- Customized Django Admin for content management
- Straightforward 'recipe' app for showcasing recipes and pictures
- Simple 'blog' app for managing posts


## Notes: Installation & Setup

### pip
pip install the dependencies found in `requirements.txt`
- `pip install -r requirements.txt`

### npm
npm install the dependencies found in `package.json`
- `npm install`

## Notes: Development
General workflow: 
- `bash ./start-project.bash` to run tests and start development server with `settings_dev.py`

Static and media files are served by AWS S3 + CloudFront

## Notes: Production
General workflow:
- run `bash ./collect-compress.bash` to collect and compress static files to `STATIC_ROOT` and `COMPRESS_ROOT` respectively, which should be AWS S3 bucket
- `git add .` or whatever you need to 
- `git commit -m "[message]"`
- `git push origin master && git push live master` -- the 2nd push is to automatically serve new files on push for remote repo on Digital Ocean (more elegant solutions exist) 
- `ssh [user]@[ip_address]`
- `sudo supervisorctl restart live`
## Notes: Database
Generally, shouldn't need to make schema changes, but if necessary, that should be handled in version control

The trickier part is how to sync up development vs production database (or maintain dedicated DB server)
