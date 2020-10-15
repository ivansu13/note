#include <linux/proc_fs.h>
#include <linux/seq_file.h>

#define BASE_DIR "test"
#define COUNT "count"

struct proc_dir_entry *base_dir

static int proc_show(struct seq_file *m, void *v)
{
    int *count = (int *)m->private;
    if (count)
        seq_printf(m, "%d", *count);
    return 0;
}

static int proc_open(struct inode *inode, struct file *file) 
{  
    return single_open(file, proc_show, PDE_DATA(inode));
}

static ssize_t proc_write(struct file *file,
		const char __user *buffer, size_t len, loff_t *pos)
{
    printk("device write\n");
    return len;
}

static const struct file_operations proc_ops= {
    .owner      = THIS_MODULE,
    .open       = proc_open,
    .read       = seq_read,
    .llseek     = seq_lseek,
    .release    = single_release,
    .write      = proc_write,
};

static int __init main_init(void)
{
    /* device init */

    // ...
    // ...
    // ...
    // ...

    base_dir = proc_mkdir(BASE_DIR, NULL);
    if (!base_dir)
        printk("Could not create dir /proc/%s\n", BASE_DIR);
    else
        proc_create_data(COUNT, 0644, base_dir, &proc_ops, (void *)&count);

    /* device init end*/
    return 0;
}

static void __exit unload(void)
{
    /* device exit */

    // ...
    // ...
    // ...

    if(base_dir) {
        remove_proc_entry(COUNT, base_dir);     
        remove_proc_entry(BASE_DIR, NULL);
    }
}

