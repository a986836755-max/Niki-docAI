# Context: temp
> @CONTEXT: Local | temp | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-30 18:57:25

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[print_js_sexp.py](print_js_sexp.py#L1)** @DEP: ndoc.atoms.ast, pathlib, sys, tree_sitter
*   **[test_js.js](test_js.js#L1)**
*   **[test_scm.py](test_scm.py#L1)** @DEP: ndoc.atoms, ndoc.atoms.ast, pathlib, sys, tree_sitter
*   **[test_ts.ts](test_ts.ts#L1)**
    *   `@API`
        *   `PUB:` CLS **User**
        *   `PUB:` CLS **UserService**
            *   `AWAIT` ASY **getUser**`(id: number) -> : Promise<User | null>`
            *   `PUB:` MET **create**`(name: string) -> : User`
*   **[verify_js.py](verify_js.py#L1)** @DEP: ndoc.atoms.scanner, pathlib, sys
*   **[verify_ts.py](verify_ts.py#L1)** @DEP: ndoc.atoms.scanner, pathlib, sys
<!-- NIKI_AUTO_Context_END -->
