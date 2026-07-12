import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const repositoryRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const skillsRoot = join(repositoryRoot, "skills", "figma-agent");
const routerRoot = join(skillsRoot, "figma-skill-router");

async function readRouterDocument(name: "SKILL.md" | "SKILLS.md") {
  return readFile(join(routerRoot, name), "utf8");
}

test("figma skill router keeps its direct-upload document identical", async () => {
  const [canonical, upload] = await Promise.all([
    readRouterDocument("SKILL.md"),
    readRouterDocument("SKILLS.md"),
  ]);

  assert.equal(upload, canonical);
});

test("figma skill router indexes every other active Figma skill", async () => {
  const [router, entries] = await Promise.all([
    readRouterDocument("SKILL.md"),
    readdir(skillsRoot, { withFileTypes: true }),
  ]);
  const listedSkills = new Set(
    [...router.matchAll(/`([a-z0-9-]+)`/g)].map((match) => match[1]),
  );
  const activeSkills = entries
    .filter((entry) => entry.isDirectory() && entry.name !== "figma-skill-router")
    .map((entry) => entry.name)
    .sort();

  assert.deepEqual(
    activeSkills.filter((skill) => !listedSkills.has(skill)),
    [],
    "every active Figma skill should be reachable from the router",
  );
  assert.match(router, /## Capability Gate/);
});
