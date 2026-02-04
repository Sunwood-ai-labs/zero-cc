import { fal } from "@fal-ai/client";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config();

fal.config({
  credentials: process.env.FAL_KEY
});

async function testVideoGen() {
  const fileData = fs.readFileSync("/workspace/projects/simple-test/inputs/starry_night.png");
  const file = new File([fileData], "starry_night.png", { type: "image/png" });
  const imageUrl = await fal.storage.upload(file);
  
  console.log("Image URL:", imageUrl);
  
  try {
    const result = await fal.subscribe("fal-ai/ltx-2/image-to-video/fast", {
      input: {
        image_url: imageUrl,
        prompt: "Stars twinkling, camera slowly pans across the night sky, shooting stars appear"
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
