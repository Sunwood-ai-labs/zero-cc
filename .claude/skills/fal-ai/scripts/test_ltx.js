import { fal } from "@fal-ai/client";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config();

fal.config({
  credentials: process.env.FAL_KEY
});

async function testVideoGen() {
  const fileData = fs.readFileSync("/workspace/projects/simple-test/inputs/winter_dusk.png");
  const file = new File([fileData], "winter_dusk.png", { type: "image/png" });
  const imageUrl = await fal.storage.upload(file);
  
  console.log("Image URL:", imageUrl);
  
  try {
    const result = await fal.subscribe("fal-ai/ltx-2/image-to-video/fast", {
      input: {
        image_url: imageUrl,
        prompt: "Gentle camera movement, snow falling slowly"
      },
      logs: true
    });
    console.log("Success!", result.data.video.url);
  } catch (error) {
    console.error("Error:", error.body || error.message);
    if (error.body && error.body.detail) {
      console.log("Detail:", JSON.stringify(error.body.detail, null, 2));
    }
  }
}

testVideoGen();
