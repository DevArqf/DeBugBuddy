from textual.app import App
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import DataTable, Footer, Header, Markdown, Static

class ResultApp(App):
    CSS = """
    Screen {
        background: #0b0f14;
        color: #e6eef8;
    }
    #main {
        padding: 1 2;
    }
    #title {
        text-style: bold;
        color: #1f6b3a;
        height: 1;
    }
    #subtitle {
        color: #3a6f4f;
        margin-bottom: 1;
        height: 1;
    }
    #sidebar {
        width: 32;
        background: #0f1622;
        border: none;
        padding: 1 1;
        margin-right: 1;
    }
    #body {
        background: #0f1520;
        border: none;
        padding: 1 2;
    }
    DataTable {
        border: none;
        background: #0f1520;
    }
    .table-title {
        color: #1f6b3a;
        text-style: bold;
        margin: 1 0 0 0;
    }
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        body: str = "",
        sidebar: str = "",
        tables: list[dict] | None = None,
    ):
        super().__init__()
        self.title_text = title
        self.subtitle_text = subtitle
        self.body_text = body
        self.sidebar_text = sidebar
        self.tables = tables or []

    def compose(self):
        yield Header(show_clock=True)
        with Container(id="main"):
            yield Static(self.title_text, id="title")
            if self.subtitle_text:
                yield Static(self.subtitle_text, id="subtitle")

            if self.sidebar_text:
                yield Horizontal(
                    Static(self.sidebar_text, id="sidebar"),
                    self._build_main_content(),
                )
            else:
                yield self._build_main_content()
        yield Footer()

    def _build_main_content(self):
        content_items = []
        if self.body_text:
            content_items.append(Markdown(self.body_text, id="body"))

        if self.tables:
            content_items.append(self._build_tables())

        if not content_items:
            content_items.append(Static("No data to display.", id="body"))

        if len(content_items) == 1:
            return content_items[0]

        return VerticalScroll(*content_items)

    def _build_tables(self):
        if len(self.tables) == 1:
            return self._table_from(self.tables[0])

        blocks = []
        for table in self.tables:
            title = table.get("title", "Table")
            blocks.append(Static(title, classes="table-title"))
            blocks.append(self._table_from(table))
        return VerticalScroll(*blocks)

    def _table_from(self, table: dict) -> DataTable:
        columns = table.get("columns", [])
        rows = table.get("rows", [])
        dt = DataTable(zebra_stripes=True)
        for column in columns:
            dt.add_column(str(column))
        for row in rows:
            dt.add_row(*[str(cell) for cell in row])
        return dt
