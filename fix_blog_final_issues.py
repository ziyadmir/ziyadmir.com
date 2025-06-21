#!/usr/bin/env python3
import re
from pathlib import Path

def fix_mermaid_and_formatting(content):
    """Fix mermaid diagrams and code block formatting issues"""
    
    # Fix broken code blocks with paragraph tags
    content = re.sub(r'<p></code></pre>', '</code></pre>', content)
    content = re.sub(r'</code></pre>\s*<p>', '</code></pre>\n\n<p>', content)
    
    # Fix code blocks that have paragraph tags inside
    content = re.sub(r'<pre class="bg-gray-100 p-4 rounded overflow-x-auto my-4"><code class="language-(\w+)">\n</p>', 
                     r'<pre class="bg-gray-100 p-4 rounded overflow-x-auto my-4"><code class="language-\1">', content)
    
    # Fix paragraph tags inside code blocks
    content = re.sub(r'<p>#', '#', content)
    content = re.sub(r'</p>\n\n<p>class', '\n\nclass', content)
    
    # Fix the specific mermaid issue in Part 6
    if "The Hidden Barrier to AI Autonomy" in content:
        # Find the section and ensure mermaid is properly formatted
        content = re.sub(
            r'<p>We measured our AI agents.*?disturbing pattern:</p>\n\n<p>',
            r'<p>We measured our AI agents\' effectiveness and found a disturbing pattern:</p>\n\n<div class="mermaid">',
            content
        )
        
        # Ensure the mermaid block is properly closed
        content = re.sub(
            r'(style E fill:#ff6b6b)\n</code></pre>',
            r'\1\n</div>',
            content
        )
    
    return content

def fix_series_navigation(content, part_num):
    """Ensure consistent series navigation styling"""
    
    # Remove any existing series-nav
    content = re.sub(r'<div class="series-nav.*?</div>\s*</article>', '</article>', content, flags=re.DOTALL)
    
    # Add consistent series navigation before closing article tag
    if part_num and part_num.isdigit():
        nav_html = get_consistent_series_nav(int(part_num))
        content = content.replace('</article>', f'\n{nav_html}\n        </article>')
    
    return content

def get_consistent_series_nav(part_num):
    """Generate consistent series navigation HTML"""
    slugs = {
        1: "ai-ide",
        2: "mcp-gateway",
        3: "ai-observability",
        4: "agent-orchestration",
        5: "knowledge-preservation",
        6: "work-as-code"
    }
    
    prev_link = ""
    next_link = ""
    
    if part_num > 1:
        prev_link = f'<a href="/blog/ai-for-work-part-{part_num-1}-{slugs[part_num-1]}.html" class="text-blue-600 hover:text-blue-800">← Part {part_num-1}</a>'
    else:
        prev_link = '<a href="/blog/ai-for-work-series-index.html" class="text-blue-600 hover:text-blue-800">← Series Overview</a>'
    
    if part_num < 6:
        next_link = f'<a href="/blog/ai-for-work-part-{part_num+1}-{slugs[part_num+1]}.html" class="text-blue-600 hover:text-blue-800">Part {part_num+1} →</a>'
    else:
        next_link = '<span class="text-gray-400">End of Series</span>'
    
    # Use the boxed style consistently
    return f'''            <div class="series-nav flex justify-between items-center">
                <div>{prev_link}</div>
                <a href="/blog/ai-for-work-series-index.html" class="text-gray-600 hover:text-gray-800">Series Index</a>
                <div>{next_link}</div>
            </div>'''

def fix_blog_post(file_path):
    """Apply all fixes to a blog post"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract part number
    part_num = None
    if 'part-' in file_path.name:
        try:
            part_num = file_path.name.split('part-')[1].split('-')[0]
        except:
            pass
    
    # Apply fixes
    content = fix_mermaid_and_formatting(content)
    
    # Fix series navigation for parts
    if part_num:
        content = fix_series_navigation(content, part_num)
    
    # Write back
    with open(file_path, 'w') as f:
        f.write(content)

# Fix Part 6 specifically for the mermaid issue
def fix_part_6_mermaid(file_path):
    """Fix the specific mermaid rendering issue in Part 6"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and fix the broken mermaid diagram
    pattern = r'<p>We measured our AI agents.*?effectiveness and found a disturbing pattern:</p>\n\n<p></code></pre>'
    replacement = '''<p>We measured our AI agents' effectiveness and found a disturbing pattern:</p>

<div class="mermaid">
graph TD
    A[AI Agent Starts Task] --> B{Can it be done via API?}
    B -->|Yes 10%| C[Agent Completes Autonomously]
    B -->|No 90%| D[Agent Asks Human]
    D --> E[Human Runs Manual Steps]
    E --> F[Human Reports Back]
    F --> G[Agent Continues]
    
    style D fill:#ff6b6b
    style E fill:#ff6b6b
</div>'''
    
    content = re.sub(pattern, replacement, content)
    
    # Fix other code block issues
    content = re.sub(r'<h3>Week 1-2: Foundation</h3>\n</code></pre>', '<h3>Week 1-2: Foundation</h3>', content)
    content = re.sub(r'<p># ', '# ', content)
    content = re.sub(r'mcp publish\n</code></pre>', 'mcp publish', content)
    
    with open(file_path, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    blog_dir = Path("/Users/ziyadmir/Desktop/code/ziyadmir.com/blog")
    
    # First fix Part 6's specific mermaid issue
    part6_path = blog_dir / "ai-for-work-part-6-work-as-code.html"
    if part6_path.exists():
        print("Fixing Part 6 mermaid issue...")
        fix_part_6_mermaid(part6_path)
    
    # Then fix all parts for consistency
    ai_posts = [
        "ai-for-work-part-1-ai-ide.html",
        "ai-for-work-part-2-mcp-gateway.html",
        "ai-for-work-part-3-ai-observability.html",
        "ai-for-work-part-4-agent-orchestration.html",
        "ai-for-work-part-5-knowledge-preservation.html",
        "ai-for-work-part-6-work-as-code.html"
    ]
    
    for post in ai_posts:
        post_path = blog_dir / post
        if post_path.exists():
            print(f"Fixing {post}...")
            fix_blog_post(post_path)
    
    print("All fixes complete!")