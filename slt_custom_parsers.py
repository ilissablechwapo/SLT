from html2ans.elements import AbstractApplicabilityLister

from builtins import str as text
from ftfy import fix_text


class ListParser(AbstractApplicabilityLister):
    supported = ['ul', 'ol']

    def parse_and_return_json(self, tag):
        if tag.name == 'ul':
            list_type = 'unordered'
        else:
            list_type = 'ordered'
        list_elements = []
        for list_item in tag.contents:
            # navigablestrings don't have contents
            if not list_item.name:
                continue

            # Recursively parse lists. Current code demands that the sublist
            # be the only element within the list item <li>.
            if len(list_item.contents) == 1:
                list_item_item = list_item.contents[0]
                if 'name' in list_item_item.__dict__ and list_item_item.name in self.supported:
                    list_elements.append(self.parse_and_return_json(list_item_item))
                    continue

            # Parse the list item as one block of text
            li_string = str(list_item)
            # SLC li are wrapped in <p> strip those out
            if li_string.startswith('<p') and not list_item.text.strip():
                continue
            if li_string.startswith('<li'):
                li_string = li_string[4:len(li_string)-5] # Strip <li></li> tags
            list_elements.append({
                "type": "text",
                "additional_properties": list_item.attrs,
                "content": li_string,
            })

        return {
            "type": "list",
            "list_type": list_type,
            "additional_properties": {k:tag.attrs[k] for k in tag.attrs},
            "items": list_elements,
        }, True