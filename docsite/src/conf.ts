const libName = "Goerr";

const links: Array<{ href: string; name: string }> = [
  { href: "/apidoc", name: "Api doc" },
  { href: "/examples", name: "Examples" },
];

// python specific
const pipPackages = [];
const pyodidePackages = [];
const examplesExtension = ".py";

export { libName, links, pipPackages, examplesExtension, pyodidePackages }