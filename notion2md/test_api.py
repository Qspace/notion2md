from notion.client import NotionClient

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2="b37e5dc60c7d94d149220ecd3b076ee596da0e0cd54b2c3d7d396e36706bca6fd334073d5a49b230f66f2224284d08ac50ae07bf12b6a8573d13d357ce9ef46adc031d1f5a1833d6c91c6ff6bc80")

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/FreeRTOS-v-Cortex-M-interrupt-76e5277bfb61442fb7c6c13940d1f016")

print("The old title is:", page.title)
for block in page.children:
    # print(block)
    print(block.type)
    if block.type == "image":
        print(block.source)