# This Cute World(Ryan4Yin's Space)

My personal blog, built using [Hugo](https://github.com/gohugoio/hugo) and hosted on [vercel](https://vercel.com/dashboard/usage) or [GitHub Pages](https://pages.github.com/).

Address: https://thiscute.world/

## Editing

Launch a local Hugo server including live reload by running (append `-F` for including future posts):

```shell
# serve in debug mode, with all drafts
hugo server -D --debug

# serve in production mode
hugo serve -e production
```

You can manually create content files (for example as `content/<CATEGORY>/<FILE>.<FORMAT>`) and provide metadata in them, however you can use the `new` command to do a few things for you (like add title and date):

```shell
hugo new posts/my-first-post.md
```

Edit the newly created file under `content/posts`, update the header of the post to say `draft: false`,
you can view the live changes in the browser http://localhost:1313/


## Github Action

Push updates to `main` branch will trigger a github action to deploy the updates automatically.

the action workflow will:

- Fetch Posts Trending Data from Google Analytics([website_statistics.json](./data/website_statistics.json)).
- Deploy to Github Pages(branch `gh-page`).
- Push Argolia Index for Search.

see [.github/workflows/gh-pages.yaml](/.github/workflows/gh-pages.yaml) for details.

