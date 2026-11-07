import { h } from "./kit/components.js";

function fact(output) {
  const found = output.status === "found";
  return h("section", { class: found ? "fact found" : "fact unavailable" }, [
    h("strong", { text: found ? `${output.value} ${output.unit}` : "Not available" }),
    h("span", { text: found ? `Source: ${output.source_id}` : "No exact corpus match" }),
  ]);
}

export default { RetrieveFactOutput: fact };
