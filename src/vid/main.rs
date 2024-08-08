use std::io::Read;
use std::io::Write;
use std::fs::File;

async fn download(url: &str) -> Result<i32, reqwest::Error> {
    // download html
    // let body = get_body(&v[i]);
    match get_body(&url).await {
        Ok(data) => {
            // 在這裡處理成功的情況，data 是取得的字串
            println!("Data: {}", data);
            // get video url
            let video_url = data.split("video_url: '").collect::<Vec<&str>>()[1].split("',").collect::<Vec<&str>>()[0];
            let video_name = data.split("<title>").collect::<Vec<&str>>()[1].split("</title>").collect::<Vec<&str>>()[0];
            let video_name = video_name.replace("/", "").replace("\\", "").replace(":", "").replace("*", "").replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "");
            let video_name = format!("{}.mp4", video_name);

            // download video
            let video_bytes = download_video(video_url).await;

            // save video
            let video_file = File::create(video_name);
            match video_file {
                Ok(mut f) => {
                    match f.write_all(&video_bytes.unwrap().to_be_bytes()) {
                        Ok(_) => {
                            println!("download success");
                        }
                        Err(error) => {
                            eprintln!("Error: {}", error);
                            eprintln!("skip {}", url);
                        }
                    }
                }
                Err(error) => {
                    eprintln!("Error: {}", error);
                    eprintln!("skip {}", url);
                }
            }
        }
        Err(error) => {
            // 在這裡處理錯誤的情況
            eprintln!("Error: {}", error);
            eprintln!("skip {}", url);
        }
    }

    Ok(1)
}

async fn get_body(url: &str) -> Result<String, reqwest::Error> {
    let body = reqwest::get(url).await?.text().await?;
    Ok(body)
}

async fn download_video(video_url: &str) -> Result<u64, reqwest::Error> {
    let video_bytes = reqwest::get(video_url).await.unwrap().content_length().unwrap();
    Ok(video_bytes)
}

fn main() {
    let mut input_file = File::open("input.txt").expect("File not found");
    let mut content = String::new();
    input_file.read_to_string(&mut content).expect("something went wrong reading the file");

    // parse input to vector
    let v: Vec<String> = content.split_whitespace().map(|s| s.to_string()).collect();
    for i in 0..v.len() {
        print!("downloading {}\n", &v[i]);
        download(&v[i]);
    }
}
