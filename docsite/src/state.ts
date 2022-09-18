import { usePython } from "usepython";
import { User } from "@snowind/state";
import { useApi } from '@snowind/api';
import { libName, pipPackages, pyodidePackages } from "./conf";
import { reactive } from "vue";

const user = new User();
const py = usePython();
const api = useApi({ serverUrl: import.meta.env.MODE === 'development' ? '' : `/${libName.toLowerCase()}` });
const state = reactive({
  apidocs: new Array<string>(),
  examples: new Array<string>(),
})

async function initPy() {
  await py.load(pyodidePackages, pipPackages)
}

function fetchIndexes() {
  api.get<Array<string>>("/apidoc/index.json").then((res) => state.apidocs = res);
  api.get<Array<string>>("/examples/index.json").then(res => state.examples = res);
}

function initState() {
  fetchIndexes()
  initPy();
}

export { py, user, initPy, api, state, initState }