import sqlite3


class DatabaseManager:

    def __init__(self):
        self._open_connection()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS clipboards (id INTEGER PRIMARY KEY, type INTEGER, content BLOB, preview TEXT);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, current_clipboard INTEGER, close_on_select INTEGER, html_as_plain_text INTEGER, stay_on_top INTEGER, opacity INTEGER);')
        self.cursor.execute('SELECT COUNT(*) FROM settings')
        if self.cursor.fetchone()[0] < 1:
            self.cursor.execute('INSERT INTO settings VALUES (0, 0, 1, 1, 1, 85)')
        self._close_connection()

    def _open_connection(self):
        self.connection = sqlite3.connect('clipboards.sqlite')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def _close_connection(self):
        self.connection.commit()
        self.connection.close()

    # Settings

    def _get_setting(self, setting):
        self._open_connection()
        self.cursor.execute('SELECT ' + setting + ' FROM settings')
        row = self.cursor.fetchone()
        self._close_connection()
        return row[0]

    def _set_setting(self, setting, value):
        self._open_connection()
        self.cursor.execute('UPDATE settings SET ' + setting + ' = ? WHERE id = 0', (value, ))
        self._close_connection()

    @property
    def current_clipboard(self):
        return self._get_setting('current_clipboard')

    @current_clipboard.setter
    def current_clipboard(self, value):
        self._set_setting('current_clipboard', value)

    @property
    def close_on_select(self, ):
        return bool(self._get_setting('close_on_select'))

    @close_on_select.setter
    def close_on_select(self, value):
        self. _set_setting('close_on_select', int(value))

    @property
    def html_as_plain_text(self):
        return bool(self._get_setting('html_as_plain_text'))

    @html_as_plain_text.setter
    def html_as_plain_text(self, value):
        self._set_setting('html_as_plain_text', int(value))

    @property
    def stay_on_top(self):
        return bool(self._get_setting('stay_on_top'))

    @stay_on_top.setter
    def stay_on_top(self, value):
        self._set_setting('stay_on_top', int(value))

    @property
    def opacity(self):
        return self._get_setting('opacity') / 100

    @opacity.setter
    def opacity(self, value):
        self._set_setting('opacity', value * 100)

    # Clipboards

    def get_next_clipboard_value(self):
        self._open_connection()
        self.cursor.execute('SELECT MAX(id) + 1 FROM clipboards')
        next_id = self.cursor.fetchone()[0]
        self._close_connection()
        return next_id

    def get_clipboard(self, clipboard_id):
        self._open_connection()
        self.cursor.execute('SELECT type, content, preview FROM clipboards WHERE id = ?', (clipboard_id,))
        data = self.cursor.fetchone()
        self._close_connection()
        if data is None:
            return None
        return {
            'type' : data['type'],
            'content' : data['content'],
            'preview' : data['preview']
        }

    def set_clipboard(self, clipboard_id, clipboard_type, clipboard_content, preview=''):
        self._open_connection()
        self.cursor.execute('INSERT OR REPLACE INTO clipboards VALUES (?, ?, ?, ?)', (clipboard_id, clipboard_type, clipboard_content, preview))
        self._close_connection()

    def remove_clipboard(self, clipboard_id):
        self._open_connection()
        self.cursor.execute('DELETE FROM clipboards WHERE id = ?', (clipboard_id,))
        self._close_connection()

    def get_clipboard_ids(self):
        self._open_connection()
        self.cursor.execute('SELECT id FROM clipboards')
        rows = self.cursor.fetchall()
        self._close_connection()
        return [row['id'] for row in rows]
