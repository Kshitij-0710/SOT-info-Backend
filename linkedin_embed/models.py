from django.db import models
from django.utils.html import mark_safe
import re

class LinkedInEmbeds(models.Model):
    embed_code = models.TextField(
        help_text="Paste LinkedIn embed iframe HTML code separated by commas"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"LinkedIn Embeds (Updated: {self.updated_at})"
    
    def preview(self):
        """Display a preview of the first embedded post in the admin"""
        if self.embed_code:
            codes = self.embed_code.split(',')
            if codes:
                first_code = codes[0].strip()
                return mark_safe(first_code)
        return "No embed code provided"
    
    def extract_urls(self):
        """Extract just the URLs from the iframe code"""
        urls = []
        if self.embed_code:
            # Split by commas first to handle multiple iframes
            codes = self.embed_code.split(',')
            for code in codes:
                # Use regex to extract the src attribute from iframe tags
                url_match = re.search(r'src=["\']([^"\']+)["\']', code.strip())
                if url_match:
                    urls.append(url_match.group(1))
        return urls
    
    preview.short_description = "Preview (First Embed)"
    
    class Meta:
        verbose_name = "LinkedIn Embeds"
        verbose_name_plural = "LinkedIn Embeds"