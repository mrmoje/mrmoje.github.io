Title: Setting up a repo cache with NGINX.
Date: 2015-12-14 03:25
Tags: nginx, proxy, cache, linux packages
Slug: repo_cache_ft_nginx
Category: Infrastructure
Author: James Nzomo
Summary: A simple how to on setting up a linux package manager repo cache for those situations where a full blown mirror would be simply overkill.


# Intro
Say you have a ton of Linux hosts package managed by apt or rpm. Maybe it's
a cluster, cloud env or just a simple learner's lab where a large groups of
(if not all) nodes will end up with the same or similar set of packages
installed and/or upgraded.

Local Linux repo mirrors would be a fantastic time & bandwidth saver for such
a setup...but the thought of dedicating double, triple or quadruple digit Gigs
(my [WAG](pages/glossary#wag) as at Dec 2015 - depending on desired distros & architectures)
and the high probability that swathes of space will go wasted on packages
no one will ever install should be enough to make you seek a more optimal
option.

What you probably want is a good repository caching proxy that initially fetches
a pkg when a host has first dibs request, then stores and serves the same pkg
for subsequent matching requests.

# The Setup
There's infinite ways to go about this. This post will cover how it's done using
webserver reverse proxy caching feature to handle requests on behalf of a few
upstream/origin repo servers.

For more info on the general idea/concept, see:-
[trafficserver][trafficserver_dox]

Though it's possible with
[Apache2](https://httpd.apache.org/docs/2.4/caching.html),
[lighthttpd](http://redmine.lighttpd.net/projects/1/wiki/Docs_ModCache) or even
[trafficserver](http://trafficserver.apache.org) we'll just go with
[NGINX](https://www.nginx.com/blog/nginx-caching-guide/) for no apparent reason.

So start by grabbing yourself some webserver:- `apt-get install nginx` and we'll sort this
out in one simple sites-available config.

### The NGINX config
The following minimal config sets nginx to handle this biz for the ubuntu
repos defined there in. Read on...this section continues inside the conf file as comments.

    :::config

    # The upstream directive defining the backend/upstream repo hosts
    # see http://nginx.org/en/docs/http/ngx_http_upstream_module.html
    # There is a primary and a backup. You can have more than that.
    # NGINX will try to load balance between them using a "weighted round-robin"
    # algorithm.
    # Most requests go to the primary, fewer to the rest.
    # Error retries trickle down the server definitions. If the last errs,
    # the result is passed on to the client.
    # By default I found that if one is unreachable during startup, nginx will
    # kaput leaving clues in the error log.
    upstream ubuntu {
      server ke.archive.ubuntu.com;
      server archive.ubuntu.com backup;
    }

    # The following directive configures the cache. Storage et all. You may want
    # the storage location  at a mount point with a filesystem on separate storage
    # device/backend to match.
    # see http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path.
    proxy_cache_path /var/repo_mirror # defines where the cache is stashed

            # defines cache path heirarchy (yaani num directory levels in cache)
            levels=1:2

            # defines name and size of zone where all cache keys and cache metadata are stashed.
            # Servers as a lookup for cached data
            keys_zone=repository_cache:50m

            # The cached data access timeout. Pkgs get nuked if no access in 14 days.
            inactive=14d

            # Cache size limit
            max_size=100g;

    # Our no-name server block
    server {

      # Keep our eyes peeled on port 80
      listen 80;

      # Location directive for the /ubuntu path
      location /ubuntu {
        # our cache's root
        root /var/repo_mirror/index_data;

        # look for packages in the following order
        try_files $uri @ubuntu;
      }

      # Location directive for the named location defined above
      location @ubuntu {

        # map this to the upstream definition above
        proxy_pass http://ubuntu;

        # 14days of caching for http code 200 response content
        proxy_cache_valid 200 14d;

        # we set our "repository_cache" zone for caching
        proxy_cache repository_cache;

        # Use stale cached data in the error events defined
        proxy_cache_use_stale error timeout invalid_header updating;

        # pass request to next (backup) server in the error events defined
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
      }
    }

The above config is by no means comprehensive but it works good enough as a demo. Feel free
to copy paste it into `/etc/nginx/sites-available/`.

One enhancement that can be made to all this is to configure a reliable storage device for
cache store.

### The client side
It goes without saying that repo related requests have to somehow be routed to the
proxy in order for all this to work.

One way is to modify the client's `/etc/apt/sources.list` or `/etc/yum.repos.d/CentOS-*.repo`
to point to our server.

Another would be to try intercept requests using various forms of MITM sorcery
like forging faux DNS replies for repo FQDNs or router configs/rules.

Since the client hosts can be configured in most cases and the latter
option is in grey area territory, we'll go with the former and modify the
repo configs. Read on to the next section for that (because the writer wrote
that before the one you reading now and he cannot be bothered to repeat
himself or make mods to the article at this point).

# Bonus vagrant-ansible deploy material
Just in case you'd like to test all this, or would like some CM to deploy the same
IRL, there is a rudimentary
["demo setup git repo"](https://github.com/mrmoje/repo_cache_plays_staring_nginx)
complete with ansible plays and a four host vagrant playground - one "repo-cacher"
and three clients - ubuntu trusty, debian jessie and CentOS 7 - which upon successful
`vagrant up`, will be provisioned to fetch their stuff from the repo-cacher.

To try it out! In case you haven't already, feel free to install latest:-
[Vagrant](https://www.vagrantup.com/downloads),
[Ansible](https://docs.ansible.com/ansible/intro_installation.html) and
[virtualbox](https://www.virtualbox.org/wiki/Downloads).
The whole #! will take a while to install, especially if running `vagrant up XXXXX`
for the first time and from a poor connection, but IMHO similar IRL bare metal
setup would probably take much longer to depoy.

Details on how the vagrant and ansible stuff comes together will be blawged in a future
post. For now, checkout the (currently empty)
[README](https://github.com/mrmoje/repo_cache_plays_staring_nginx/blob/master/README.md)
or just run `vagrant up repo-cache` to launch the repo cache then `vagrant ssh repo-cache`
and open `/etc/nginx/sites-available/repo-cache.conf`.

Have a look at the tri-distro proxy cache config and feel free to mod as you please.
Reset it all by running `vagrant provision repo-cache`

You should also be able to browse the upstream repos via the proxy from the following links:-

 - <http://repo-cache.local/ubuntu/>
 - <http://repo-cache.local/debian/>
 - <http://repo-cache.local/centos/>

__NB__: Replace the hostname with `10.64.0.2` if you dont have a mdns client installed.


You can subsequently launch one, two or all of the other client hosts
`vagrant up repo-cache ubuntu #(or debian or centos)`. Feel free to `vagrant ssh` into
them, take a look at `/etc/apt/sources.list` or `/etc/yum.repos.d/CentOS-*.repo` and
give some package installs a run. Don't forget to peek at `repo-cache:/var/repo_mirror`
while you do that.

Look at the [Vagrant](https://github.com/mrmoje/repo_cache_plays_ft_nginx/blob/master/Vagrantfile)
file to see hodge-podge of provisioning methods and the
[sedding](https://www.gnu.org/software/sed/manual/sed.html) that swaps the vanilla repos
for our example proxy.


# Outro
We put a [variant of this proxy-cache](https://github.com/kili/playbooks/blob/master/playbooks/repository_cache.yaml)
method to good use at a cloud compute startup I used to work for and it worked
out well for us and our tenants.

In the end amongst other benefits, we were (obviously) able to reduce latency and
network traffic (by how much is anyones guess. We didn't care measure).
We also ended up with more space to put to good use. Space that would have otherwise
been taken up by a multi repo mirror.

The only possible downside I can fathom for this is that it will still
take longer for the first host/request to get sorted which may be bad for
the installing party depending on how pressed for time they are, but then again
with life, every now and then, somebody has to take one for the team. C'est la Vie!

### Resources, Refs & google juice:-
  - [Trafficserver dox on reverse proxy][trafficserver_dox]
  - [NGINX proxy module documentation][NGINX_proxy_dox]
  - An excelent tut on caching with nginx with video & docker hands-on:- <http://czerasz.com/2015/03/30/nginx-caching-tutorial/>

[trafficserver_dox]:(https://trafficserver.readthedocs.org/en/5.3.x/admin/reverse-proxy-http-redirects.en.html)
[NGINX_proxy_dox]:(http://nginx.org/en/docs/http/ngx_http_proxy_module.html)
[NGINX_cache_guide]:(https://www.nginx.com/blog/nginx-caching-guide/)

[arbitrary case-insensitive reference text]: https://www.mozilla.org
