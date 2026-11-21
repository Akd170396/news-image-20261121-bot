// Entry point for the news-image-20261121 bounty entry.
//
// The infographic itself is drawn offline by render.py and committed to the
// repository as entry.png. At grade time this program simply copies those
// exact bytes to the output directory, so both harness runs write identical
// output (no network, no clock, no randomness).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(repoRoot, "entry.png");
// The grader mounts a writable /output; local checks point MAKEFUN_OUTPUT_DIR
// at a scratch folder instead.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destination = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImage, destination);
console.log(`news-image-20261121: copied entry.png to ${destination}`);
