# usage

## Python script

- Download all artist's album that user has followed

```bash
python3 script.py all --username <your_username>
```

- Download all artist's album that user has followed with multi-thread

```bash
python3 script.py all --username <your_username> --multi_thread
```

- Download artist's all album

```bash
python3 script.py artist --artist_url https://<artist>.bandcamp.com
```

- Download single album

```bash
python3 script.py album --album_url https://<artist>.bandcamp.com/album/<albumname>
```

## Rust binary

- Download all artist's album that user has followed

```bash
cargo run all username
```

- Download all artist's album that user has followed with multi-thread

```bash
cargo run all username --multi_thread
```

- Download artist's all album

```bash
cargo run artist artist_url
```

- Download single album

```bash
cargo run album album_url
```s