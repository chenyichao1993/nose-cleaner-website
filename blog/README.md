# Nose Cleaner Blog

This is the blog section of the Nose Cleaner website, built with Jekyll and hosted on Cloudflare Pages.

## Features

- **Jekyll-based static blog** - Fast, secure, and SEO-friendly
- **Responsive design** - Works on all devices
- **SEO optimized** - Structured data, meta tags, and sitemaps
- **RSS feed** - Automatic feed generation
- **Category and tag support** - Organized content
- **Social sharing** - Easy sharing on social media
- **Newsletter integration** - Email subscription support

## Content Structure

### Categories
- Baby Care
- Adult Care
- Product Reviews
- Safety Tips
- How-to Guides
- Seasonal Care

### Tags
- baby nose cleaner
- nasal irrigation
- nasal aspirator
- safety tips
- product comparison
- allergy relief
- cold and flu
- nasal health

## Adding New Posts

1. Create a new file in `_posts/` with the format: `YYYY-MM-DD-title.md`
2. Add front matter with required fields:
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   description: "Brief description for SEO"
   date: 2025-01-06
   author: "Nose Cleaner Team"
   categories: ["Category Name"]
   tags: ["tag1", "tag2"]
   image: "/images/webp/your-image.webp"
   toc: true
   ---
   ```
3. Write your content in Markdown
4. Commit and push to GitHub

## Local Development

1. Install Jekyll: `gem install jekyll bundler`
2. Install dependencies: `bundle install`
3. Run locally: `bundle exec jekyll serve`
4. View at: `http://localhost:4000/blog/`

## Deployment

The blog is automatically deployed to Cloudflare Pages when changes are pushed to the main branch.

## SEO Features

- **Structured data** - Article schema for better search results
- **Meta tags** - Optimized title, description, and Open Graph tags
- **Sitemap** - Automatic XML sitemap generation
- **RSS feed** - Feed for subscribers
- **Canonical URLs** - Prevents duplicate content issues
- **Image optimization** - WebP format and proper alt tags

## Analytics

The blog includes:
- Google Analytics 4
- Google Tag Manager
- Microsoft Clarity
- Baidu Analytics

## Contact

For questions about the blog, contact: motionjoy93@gmail.com
