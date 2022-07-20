# iStub

Validator for type annotations.

- [ ] Stubs generation
- [x] Code style checking with `flake8`
- [x] Type checking with `mypy` and `pyright`
- [x] Type consistency checking with `mypy.stubtest`

## Usage

### Basic usage

Let's assume that you want to check `mylib-stubs` package against `mylib`

Create a file `istub.yml` in your project root:

```yaml
packages:
  - name: mylib
    path: ./mylib-stubs
    checks:
        mypy: true
        stubtest: true
```

Run checker:

```bash
python -m istub
```

You can create a whitelist of acceptable errors:

```bash
python -m istub --update
```

## Latest changes

Full changelog can be found in [Releases](https://github.com/youtype/istub/releases).

## Versioning

`istub` version follows
[PEP 440](https://www.python.org/dev/peps/pep-0440/) format.

## Support and contributing

Please reports any bugs or request new features in
[istub](https://github.com/youtype/istub/issues/) repository.
