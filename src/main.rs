use std::fs;
use image;

const NUM_CHANNELS: usize = 3;

macro_rules! SubtractPixels {
    ($pixel1:expr, $pixel2:expr, $return:expr, $return_len:expr) => {
        for i in 0..NUM_CHANNELS
            {$return[i]+=i32::abs($pixel1[i] as i32 - $pixel2[i] as i32) as u32;}
        $return_len+=1;
    };
}

macro_rules! GetPixAvg {
    ($pixels:expr, $pixels_len:expr, $return:expr) => {
        for i in 0..NUM_CHANNELS 
            {$return[i]/=$pixels_len as u32;}
    };
}

macro_rules! GetSamples {
    ($img:expr, $x:expr, $y:expr, $dimensions:expr, $return:expr, $return_len:expr) => {
            let true_x: i32 = $x as i32 - 1; let true_y: i32 = $y as i32 - 1;
            for i in 0..NUM_CHANNELS { for j in 0..NUM_CHANNELS {
                let sample_x: i32 = true_x + i as i32; let sample_y: i32 = true_y + j as i32;
                if ((sample_x > 0) && (sample_x < $dimensions.0 as i32)) && ((sample_y > 0) && (sample_y < $dimensions.1 as i32)) {
                    let mut pixel_dat: [u32; NUM_CHANNELS] = [0; NUM_CHANNELS];
                    if (sample_x >= 0) && (sample_y >= 0) { for k in 0..NUM_CHANNELS // This right here is the problem
                        {pixel_dat[k] = $img.get_pixel(sample_x as u32, sample_y as u32).0[k] as u32;}
                    $return[$return_len] = pixel_dat;
                    $return_len+=1;
                }
            }}
        }
    };
}

macro_rules! CalcAvgDiff {
    ($samples:expr, $samples_len:expr, $return:expr) => {
        let mut differences_len: usize = 0;
        
        for i in 0..$samples_len { for j in 0..$samples_len 
            {SubtractPixels!($samples[i], $samples[j], $return, differences_len);}}
        
        GetPixAvg!($return, differences_len, $return);
    };
}

macro_rules! Sample {
    ($img:expr, $x:expr, $y:expr, $dimensions:expr, $avg_diff_to_draw_pix:expr, $return:expr) => {
            let mut samples_len: usize = 0;
            let mut samples: [[u32; NUM_CHANNELS]; 9] = [[0; NUM_CHANNELS]; 9];
            GetSamples!($img, $x, $y, $dimensions, samples, samples_len);
            
            let mut avg: [u32; NUM_CHANNELS] = [0; NUM_CHANNELS]; 
            CalcAvgDiff!(samples, samples_len, avg);
            
            let mut avg_val: u32 = 0;
            for i in 0..NUM_CHANNELS
                {avg_val+=avg[i];}
            avg_val/=avg.len() as u32;
        
            *$return.get_pixel_mut($x, $y) = image::Rgb([255 * !(avg_val > $avg_diff_to_draw_pix) as u8; NUM_CHANNELS]);
    };
}

const IMG_NAME_TXT: &str = "img_name.txt";
const PIXEL_DRAWING_SETTINGS_NAME: &str = "pixel_drawing_settings.txt";
const OUTPUT_NAME: &str = "output.jpeg";

fn main() {
    println!("Getting the pixel drawing settings...");
    let pixel_drawing_settings_txt: String = fs::read_to_string(PIXEL_DRAWING_SETTINGS_NAME)
        .expect(format!("ERROR: Something went wrong when trying to read the pixel drawing settings from {}!", PIXEL_DRAWING_SETTINGS_NAME).as_str())
            .trim().to_string();
    println!("Getting avg_diff_to_draw_pix...");
    let avg_diff_to_draw_pix: u32 = pixel_drawing_settings_txt.parse::<u32>()
        .expect("ERROR: Something went wrong when trying to parse setting avg_diff_to_draw_pix into an u32");
    println!("Got avg_diff_to_draw_pix as {}!", avg_diff_to_draw_pix);
    println!("Got the pixel drawing settings!");

    println!("Getting image's name...");
    let img_name: String = fs::read_to_string(IMG_NAME_TXT)
        .expect(format!("ERROR: Something went wrong when trying to read the image's name from {}!", IMG_NAME_TXT).as_str())
            .trim().to_string();
    println!("Got the image's name! The image's name is {}", &img_name);

    println!("Getting {}...", &img_name);
    let img: image::RgbImage = image::open(&img_name)
        .expect("ERROR: Wasn't able to retrieve the imag!").to_rgb8();
    println!("Got {}!", &img_name);

    println!("Getting {}'s dimensions...", &img_name);
    let dimensions: (u32, u32) = img.dimensions();
    println!("Got {}'s dimensions!", &img_name);

    println!("{}'s dimensions:", &img_name);
    let dimension_names: [&str; 2] = ["width", "height"];
    let dimensions_array: [u32; 2] = [dimensions.0, dimensions.1];
    for i in 0..2
        {println!("    {}: {}", dimension_names[i], dimensions_array[i]);}

    println!("Creating output buffer...");
    let mut output: image::RgbImage = image::RgbImage::new(dimensions.0, dimensions.1);
    println!("Created output buffer!");

    println!("Processing image...");
    for i in 0..dimensions.0 { for j in 0..dimensions.1
        {Sample!(img, i, j, dimensions, avg_diff_to_draw_pix, output);}}
    println!("Processed image!");

    println!("Saving image to {}...", OUTPUT_NAME);
    output.save(OUTPUT_NAME).expect("ERROR: Something went wrong when trying to save the output to ");
    println!("Saved image to {}!", OUTPUT_NAME);
}
