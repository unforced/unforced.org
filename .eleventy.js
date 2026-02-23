module.exports = function(eleventyConfig) {
  // Copy static assets (paths relative to input directory)
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  eleventyConfig.addPassthroughCopy({ "src/images": "images" });
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });

  // Create posts collection from writing folder
  eleventyConfig.addCollection("posts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/writing/*.md")
      .filter(post => !post.data.draft)
      .sort((a, b) => b.date - a.date);
  });

  // Date formatting filters
  eleventyConfig.addFilter("formatDate", (date) => {
    const d = new Date(date);
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return `${months[d.getMonth()]} ${d.getFullYear()}`;
  });

  eleventyConfig.addFilter("formatDateFull", (date) => {
    const d = new Date(date);
    const months = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"];
    return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  });

  eleventyConfig.addFilter("isoDate", (date) => {
    return new Date(date).toISOString();
  });

  // Get year from date for grouping
  eleventyConfig.addFilter("getYear", (date) => {
    return new Date(date).getFullYear();
  });

  // Limit filter for arrays
  eleventyConfig.addFilter("limit", (array, limit) => {
    return array.slice(0, limit);
  });

  // Excerpt filter - get first paragraph
  eleventyConfig.addFilter("excerpt", (content) => {
    if (!content) return "";
    // Remove HTML tags and get first paragraph
    const text = content.replace(/<[^>]+>/g, '');
    const firstPara = text.split('\n\n')[0];
    // Limit to ~160 chars for meta descriptions
    if (firstPara.length > 160) {
      return firstPara.substring(0, 157) + "...";
    }
    return firstPara;
  });

  // Dev server config - bind to 0.0.0.0 for network access
  eleventyConfig.setServerOptions({
    liveReload: true,
    domDiff: true,
    port: 8080,
    watch: [],
    showAllHosts: true,
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts"
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
