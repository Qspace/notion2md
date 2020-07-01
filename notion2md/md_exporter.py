import notion
import os
from notion.client import NotionClient

def get_page():
    token_v2 = input("Token_v2: ")
    url = input("Notion Page Url: ")
    return token_v2,url

def set_filename():
    directory = './output/'
    if not(os.path.isdir(directory)):
        os.makedirs(os.path.join(directory))
    fname = input("Markdown file name: ") + ".md"
    fname = os.path.join(directory,fname)
    return fname

def recursive_getblocks(block,container,client):
    container.append(client.get_block(block.id))
    try:
        for children_id in block.get("content"):
            children = client.get_block(children_id)
            recursive_getblocks(children,container,client)
    except:
        return

def link(name,url):
    return "["+name+"]"+"("+url+")"

def block2md(blocks):
    md = ""
    numbered_list_index = 0
    for block in blocks:
        btype = block.type
        if btype != "numbered_list":
            numbered_list_index = 0
        try:
            bt = block.title
        except:
            pass
        if btype == 'header':
            md += "# " + bt
        elif btype == "sub_header":
            md += "## " +bt
        elif btype == "sub_sub_header":
            md += "### " +bt
        elif btype == 'page':
            try:
                if "https:" in block.icon:
                    icon = "!"+link("",block.icon)
                else:
                    icon = block.icon
                md += "# " + icon + bt
            except:
                md += "# " + bt
        elif btype == 'text':
            md += bt
        elif btype == 'bookmark':
            md += link(bt,block.link)
        elif btype == "video" or btype == "file" or btype =="audio" or btype =="pdf" or btype == "gist":
            md += link(block.source,block.source)
        elif btype == "bulleted_list" or btype == "toggle":
            md += '- '+bt
        elif btype == "numbered_list":
            numbered_list_index += 1
            md += str(numbered_list_index)+'. ' + bt
        elif btype == "image":
            md += "!"+link(block.source,block.source)
        elif btype == "code":
            md += "```"+block.language+"\n"+block.title+"\n```"
        elif btype == "equation":
            md += "$$"+block.latex+"$$"
        elif btype == "divider":
            md += "---"
        elif btype == "to_do":
            if block.checked:
                md += "- [x] "+ bt
            else:
                md += "- [ ]" + bt
        elif btype == "quote":
            md += "> "+bt
        elif btype == "column" or btype =="column_list":
            continue
        else:
            pass
        md += "\n"
    return md

def export():
    fname = set_filename()
    file = open(fname,'w')
    token_v2, url = get_page()
    blocks = []

    client = NotionClient(token_v2 = token_v2)
    page = client.get_block(url)

    recursive_getblocks(page,blocks,client)
    md = block2md(blocks)

    file.write(md)
    file.close()

    print("The markdown extraction is complete.")

if __name__ == "__main__":
    export()