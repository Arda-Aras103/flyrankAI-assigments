# DNS Walkthrough

When I type a website address, my browser needs to find the server that can answer for that name. DNS is the directory that connects readable domain names to the network addresses computers use. It does not move the web page itself; it helps the browser find where to ask for it.

The first stop is usually a **recursive resolver**, often run by my internet provider or a public DNS service. It checks whether it already has a recent answer in its cache. If not, it follows the DNS hierarchy: it asks a **root nameserver** where to find the `.app` nameservers, asks a `.app` nameserver which nameservers are authoritative for `netlify.app`, and asks one of those **authoritative nameservers** for the requested hostname. The authoritative server is the source that publishes the DNS records for that part of the domain.

For a custom site address, the record might be a **CNAME**. A CNAME says that one hostname is another hostname’s alias. For example, `www.example.com` could point to `my-site.netlify.app`. The resolver then looks up the target name to find its address. A CNAME is not a redirect: the browser still shows the address the visitor typed. A DNS record also has a time-to-live (TTL), so resolvers may keep a valid answer in cache for that long before asking again. This is why a DNS change can take time to appear everywhere.

After DNS gives the browser an IP address, the browser connects to the hosting service. For an HTTPS address, it also checks the site’s TLS certificate so it can confirm the connection is encrypted and the certificate matches the hostname. The browser then asks for the page, and the host sends back the HTML, CSS, and other files. In short: the resolver finds the answer, nameservers publish it, the record describes the name or alias, and the host returns the website.

My current `*.netlify.app` address is supplied by Netlify, so I do not need to buy a domain or add a CNAME for this assignment. If I connect a domain later, I will use the exact DNS records Netlify gives me, then wait for the record to propagate and confirm the new address loads over HTTPS.
