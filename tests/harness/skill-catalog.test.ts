import { describe, expect, it } from "vitest";
import { AcceptanceCriteriaLoader } from "./criteria-loader.js";
import { SkillCopilotClient } from "./copilot-client.js";

const repoRoot = new URL("../../", import.meta.url).pathname.replace(/\/$/, "");

describe("revamped skills catalog", () => {
  it("discovers active SKILLS.md skills and excludes the archive", () => {
    const loader = new AcceptanceCriteriaLoader(repoRoot);
    const skills = loader.listSkillsWithCriteria();

    expect(skills).toContain("figma-agent/accessibility-audit");
    expect(skills).not.toContain("archive/rlm");
  });

  it("loads SKILLS.md as generation context", () => {
    const client = new SkillCopilotClient(repoRoot, true);
    const context = client.loadSkillContext("figma-agent/accessibility-audit");

    expect(context).toContain("accessibility-audit");
    expect(context).toContain("SKILLS.md");
  });
});
