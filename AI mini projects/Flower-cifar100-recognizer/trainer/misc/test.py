import wandb
import torch


class Test:

    def __init__(self, model, test_loader, device, save_path, test_run=20, wandb_needed=False):
        self.model = model
        self.test_loader = test_loader
        self.device = device
        self.save_path = save_path
        self.test_run = test_run
        self.wandb = wandb_needed
        self.image_set, self.label_set, self.pred_set = [], [], []
    
    def load(self):
        checkpoint = torch.load(self.save_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])

    def test(self, config_save_model_path=None):
        self.load()
        self.model.eval()
        for step, (images, labels) in enumerate(self.test_loader):
            with torch.no_grad():
                images, labels = images.to(self.device).float(), labels.to(self.device).float()
                outputs = self.model(images)
                self.pred_set.append(outputs)
                self.label_set.append(labels)
                self.image_set.append(images)
            if step+1 == self.test_run:
                break
        if self.wandb:
            wandb.save(self.save_path)
            torch.onnx.export(self.model, images, config_save_model_path)
            wandb.save(config_save_model_path)
        return self.image_set, self.label_set, self.pred_set, self.model