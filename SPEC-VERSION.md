# Spec version

`0.1`

This is the format version that the rules, schemas, jobs and connection files in
this repository are written against. Every job manifest declares the version it
targets. A workspace records the version it was created under in its own
`cos-workspace.yaml`; the product-local `cos-os.yaml` records the product version
and the path connecting the two folders.

When the format changes in a way that affects existing workspaces, the version
moves up and the change ships with a migration note in [CHANGELOG.md](CHANGELOG.md)
— what changes, how to apply it, how to undo it. Never a silent change.
