module.exports = {
    root: true,
    env: { browser: true, es2020: true },

    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended-type-checked",
        "plugin:@typescript-eslint/stylistic-type-checked",
    ],

    ignorePatterns: ["dist", ".eslintrc.cjs", "index.html"],

    parser: "@typescript-eslint/parser",
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        project: ["./tsconfig.json"],
        tsconfigRootDir: __dirname,
    },

    plugins: ["@stylistic/ts"],

    rules: {
        "@stylistic/ts/indent": ["warn", 4],

        "max-len": [
            "warn",
            {
                "code": 140
            }
        ],

        "@typescript-eslint/consistent-type-definitions": ["warn", "type"],

        "@typescript-eslint/no-unused-vars": [
            "warn",
            {
                "args": "all",
                "argsIgnorePattern": "^_",
                "caughtErrors": "all",
                "caughtErrorsIgnorePattern": "^_",
                "destructuredArrayIgnorePattern": "^_",
                "varsIgnorePattern": "^_",
                "ignoreRestSiblings": true
            }
        ],

        "quotes": [
            "warn",
            "double",
            {
                "avoidEscape": true,
                "allowTemplateLiterals": true
            }
        ],

        "semi": ["warn", "always"]
    },
}
