# Documentation surfaces to check

For every behavioral change, check each surface below. A surface that does not
exist in the project is skipped, not created, unless the user asked for it.

## README.md
- Feature list and project description.
- Installation and setup steps: still correct after dependency or config changes?
- Usage examples and commands: still runnable exactly as written?
- Environment variables and prerequisites.

## API documentation
- Endpoint lists, request and response examples, status codes.
- Generated specs (OpenAPI, GraphQL schema): regenerate if the project has a
  generation command; never hand-edit generated files.

## Docstrings and code comments
- Docstrings of every function whose signature or behavior changed.
- Comments that describe the old behavior near changed lines.

## Configuration samples
- `.env.example` and sample config files: new keys added, removed keys deleted.
- Default values mentioned in docs match the code's actual defaults.

## CHANGELOG.md
- One entry per user-visible change, under the unreleased section, in the
  file's existing format. Skip if the project keeps no changelog.

## Contributor docs
- CONTRIBUTING.md, docs/ folder guides: build, test, and run instructions
  still correct.
- CLAUDE.md: update only facts that changed (commands, structure, conventions);
  keep it short.
