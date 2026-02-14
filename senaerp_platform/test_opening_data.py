import frappe

def test_opening_data():
    openings = frappe.get_all(
        'Opening',
        filters={'is_active': 1},
        fields=['name', 'title', 'job_description'],
        limit=1
    )

    if openings:
        job_desc = openings[0]['job_description']
        print('='*50)
        print('Type:', type(job_desc))
        print('='*50)
        print('First 500 characters:')
        print(repr(job_desc[:500]))
        print('='*50)
        print('Actual display (first 300 chars):')
        print(job_desc[:300])
        print('='*50)

        # Check if it contains actual HTML tags
        if '<h3>' in job_desc:
            print('✓ Contains <h3> tags')
        else:
            print('✗ No <h3> tags found')

        if '&lt;' in job_desc:
            print('✗ HTML is ESCAPED (contains &lt;)')
        else:
            print('✓ HTML is NOT escaped')
    else:
        print('No openings found')
