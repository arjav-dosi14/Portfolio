import re
import sys

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add "All Technologies" button
    button_html = '''<h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">Technical Arsenal</h2>
            <div class="h-px w-8 bg-gray-300 mb-6"></div>
            <button id="clear-filter-btn" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-[13px] font-semibold rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm" aria-label="Show All Technologies">
                All Technologies
            </button>'''
    content = re.sub(r'<h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">Technical Arsenal</h2>\s*<div class="h-px w-8 bg-gray-300"></div>', button_html, content)

    # 2. Add attributes to skill items
    # We look for: <!-- SkillName --> \n <div class="relative flex flex-col items-center justify-center w-full">
    # And we replace the div with the added attributes.
    
    # Mapping of alt texts or comments to filter tags
    skills = {
        'Python': 'python',
        'Java': 'java',
        'C/C++': 'c',
        'HTML5': 'html',
        'MySQL': 'mysql',
        'OOP': 'oop',
        'NumPy': 'numpy',
        'Pandas': 'pandas',
        'File & Exception Handling': 'file-handling',
        'JDBC': 'jdbc',
        'JSP': 'jsp',
        'DSA': 'dsa',
        'Artificial Intelligence': 'ai'
    }

    for skill_name, tag in skills.items():
        # Match <!-- SkillName -->
        # <div class="relative flex flex-col items-center justify-center w-full">
        escaped_name = re.escape(skill_name)
        pattern = r'(<!-- ' + escaped_name + r' -->\s*)<div class="relative flex flex-col items-center justify-center w-full">'
        replacement = r'\1<div class="relative flex flex-col items-center justify-center w-full skill-filter-btn cursor-pointer transition-all duration-300" data-filter="' + tag + r'" role="button" tabindex="0" aria-pressed="false" aria-label="Filter by ' + tag + '">'
        content = re.sub(pattern, replacement, content)
        
        # Also remove cursor-default from the img inside the skill to allow cursor-pointer to take over
        # We find the img that comes right after this div. This is a bit tricky with regex, so let's just globally replace cursor-default for these specific images.
        # Actually, let's leave cursor-default alone and let CSS handle it, or replace cursor-default with cursor-pointer in the skill imgs.
        # The prompt says: "Use cursor: pointer. The entire skill block (icon + label) should be clickable, not just the icon."
        # If we put cursor-pointer on the parent, we must remove cursor-default from the image.
    content = re.sub(r'(class="[^"]*)cursor-default([^"]*")', r'\1\2', content)

    # 3. Add Status Text to Featured Projects
    status_text_html = '''<h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">Featured Projects</h2>
            <div class="h-px w-8 bg-gray-300 mb-6"></div>
            <p id="project-filter-status" class="text-[14px] text-gray-500 font-medium" aria-live="polite">Showing all projects</p>'''
    content = re.sub(r'<h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">Featured Projects</h2>\s*<div class="h-px w-8 bg-gray-300"></div>', status_text_html, content)

    # 4. Add data-tags to projects
    # ShopSphere
    content = re.sub(r'(<!-- Project 1: ShopSphere -->\s*)<div\s*class="([^"]*)"', r'\1<div class="\2 project-card" data-tags="python html mysql django file-handling"', content)
    # Laptix
    content = re.sub(r'(<!-- Project 2: Laptix -->\s*)<div\s*class="([^"]*)"', r'\1<div class="\2 project-card" data-tags="python html django"', content)
    # Hospital System
    content = re.sub(r'(<!-- Project 3: Hospital System -->\s*)<div\s*class="([^"]*)"', r'\1<div class="\2 project-card" data-tags="java jsp mysql oop"', content)

    # 5. Add Script at the end before {% endblock %} or </body>
    script_content = """
<!-- Project Filtering Script -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.skill-filter-btn');
    const clearBtn = document.getElementById('clear-filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    const statusText = document.getElementById('project-filter-status');
    const projectsSection = document.getElementById('projects');

    let activeFilter = null;

    function updateProjects(filterTag) {
        let matchCount = 0;
        let activeTagLabel = '';

        if (filterTag) {
            // Find the active button to get its label for the status text
            const activeBtn = Array.from(filterBtns).find(btn => btn.getAttribute('data-filter') === filterTag);
            if (activeBtn) {
                activeTagLabel = activeBtn.querySelector('img').getAttribute('alt') || filterTag;
            }
        }

        projectCards.forEach(card => {
            const tags = (card.getAttribute('data-tags') || '').split(' ');
            const matches = !filterTag || tags.includes(filterTag);
            
            if (matches) {
                matchCount++;
                card.style.display = 'flex'; // original display
                // Force reflow
                card.offsetHeight;
                card.style.opacity = '1';
                card.style.transform = 'scale(1) translateY(0)';
            } else {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.95) translateY(10px)';
                // wait for transition then hide
                setTimeout(() => {
                    if (card.style.opacity === '0') {
                        card.style.display = 'none';
                    }
                }, 300);
            }
        });

        // Update status text
        if (!filterTag) {
            statusText.textContent = 'Showing all projects';
        } else {
            statusText.textContent = `Showing ${matchCount} ${activeTagLabel} project${matchCount !== 1 ? 's' : ''}`;
        }
    }

    function applyFilter(filterTag) {
        if (activeFilter === filterTag) {
            // Toggle off
            activeFilter = null;
        } else {
            activeFilter = filterTag;
        }

        filterBtns.forEach(btn => {
            const tag = btn.getAttribute('data-filter');
            const img = btn.querySelector('img');
            if (activeFilter === null) {
                // Reset to default
                btn.classList.remove('opacity-70', 'scale-[1.05]', 'drop-shadow-[0_0_12px_rgba(59,130,246,0.8)]', 'active-filter');
                btn.setAttribute('aria-pressed', 'false');
                if (img) img.classList.remove('grayscale-0', 'opacity-100');
            } else if (tag === activeFilter) {
                // Active
                btn.classList.remove('opacity-70');
                btn.classList.add('scale-[1.05]', 'drop-shadow-[0_0_12px_rgba(59,130,246,0.8)]', 'active-filter');
                btn.setAttribute('aria-pressed', 'true');
                if (img) img.classList.add('grayscale-0', 'opacity-100');
            } else {
                // Inactive
                btn.classList.remove('scale-[1.05]', 'drop-shadow-[0_0_12px_rgba(59,130,246,0.8)]', 'active-filter');
                btn.classList.add('opacity-70');
                btn.setAttribute('aria-pressed', 'false');
                if (img) img.classList.remove('grayscale-0', 'opacity-100');
            }
        });

        updateProjects(activeFilter);

        // Smooth scroll to projects if a filter was selected
        if (activeFilter && projectsSection) {
            projectsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tag = btn.getAttribute('data-filter');
            applyFilter(tag);
        });

        btn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const tag = btn.getAttribute('data-filter');
                applyFilter(tag);
            }
        });
    });

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            applyFilter(null);
        });
    }
});
</script>
"""
    
    # ensure project cards have smooth transition
    content = re.sub(r'transition-all duration-300', r'transition-all duration-300 ease-in-out', content)

    if filepath.endswith('templates\\index.html') or filepath.endswith('templates/index.html'):
        content = content.replace('{% endblock %}', script_content + '\n{% endblock %}')
    else:
        # docs/index.html
        content = content.replace('</body>', script_content + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed {filepath}")

process_file(r'c:\Users\ARJAV\PycharmProjects\Portfolio\templates\index.html')
process_file(r'c:\Users\ARJAV\PycharmProjects\Portfolio\docs\index.html')
