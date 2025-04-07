social_media_prompt = """Below is information about the company's product.
Product Description: {product_description}
Competitive Advantage: {competitive_advantage}
Price: {price}

You may also be given an image of the product for reference.

Using the image and information provided, create a short, compelling social media ad caption that is catchy and has a clear call to action (i.e. subscribe to newsletter, find out more, buy now). Include just the generated ad caption, and nothing else."""

blog_post_prompt = """Below is information about the company's product.
Product Description: {product_description}
Competitive Advantage: {competitive_advantage}
Price: {price}
        
You may also be given an image of the product for reference.

Using the image and information provided, create a blog post that naturally & indirectly markets the product. Include just the generated blog post, and nothing else."""

email_campaign_prompt = """Below is information about the company's product.
Product Description: {product_description}
Competitive Advantage: {competitive_advantage}
Price: {price}

You may also be given an image of the product for reference.

Using the image and information provided, create a catchy email campaign that hooks potential buyers into buying a product or clicking into the company's website. Include just the generated email campaign, and nothing else."""