# Web-content-filler
带有轻量SEO的网站爬虫（typecho）

支持SEO、又拍云上传图片、替换链接、转Markdown、提取关键词
**仅限typecho网站填充内容**

需要修改/var/Widget/XmlRpc.php文件，添加
$input['date'] = trim($content['date']) == NULL ? _t('') : $content['date'];
