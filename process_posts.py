
from math import ceil
from pathlib import Path
import datetime as dt

# pip3 install pyyaml
import yaml

POSTS_DIR = Path(__file__).parent / "content/posts/"

def get_all_posts():
    """
    遍历位于 posts 中所有的 Markdown 文档
    """
    return list(POSTS_DIR.glob("**/*.md"))


def parse_post_metadata(path: Path):
    """
    解析 Markdown 头部的 hugo metadata 信息
    """
    with path.open("r", encoding="utf-8") as f:
        metadata_lines = [f.readline()]
        for line in f:
            if line.strip(" ").strip("\n") != "---":
                metadata_lines.append(line)
            else:
                # it's the end of markdown metadata
                return yaml.safe_load("".join(metadata_lines))


def gen_folder_name(post: Path):
    """
    生成新的父目录名称，后续会将 posts 移动到此目录中

    生成规则举例：
    1. 按 年/月-日 或者 年/季度 对文章进行分类
    2. 按词云的权重或者相似度对文章进行智能分类
    3. 其他...
    """
    post_metadata = parse_post_metadata(post)
    post_time: dt.datetime = post_metadata['date']

    quater = ceil(post_time.month / 4)

    # 目前暂按 年/季度 进行分类
    return f"{post_time.year}/Q{quater}"


def restructure_posts(posts):
    processed_files = []
    for p in posts:
        if p in processed_files:
            continue

        # 新的 Posts 父目录
        new_post_dir = POSTS_DIR / gen_folder_name(p)
        new_post_dir.mkdir(parents=True, exist_ok=True)

        # 将 posts 的所有文件移动到新的位置
        for file in p.parent.iterdir():
            processed_files.append(file)

            new_parent = new_post_dir / file.parent.name
            new_parent.mkdir(parents=True, exist_ok=True)
            new_path = new_parent / file.name

            print(new_path)
            file.rename(new_path)
        
        if not any(p.parent.iterdir()):
            # 删除 post 空的旧目录
            p.parent.rmdir()


def main():
    posts = get_all_posts()
    # 调整 posts 文件夹结构
    restructure_posts(posts)

    # 更多新功能待开发

if __name__ == "__main__":
    main()
